#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional, List
from dagster import get_dagster_logger
from dagster import Definitions
from dagster import AssetExecutionContext
from dagster import DefaultScheduleStatus
from dagster import ScheduleDefinition
from dagster import define_asset_job
from dagster_dbt import DbtCliResource
from dagster_dbt import dbt_assets
from dagster_dbt import build_dbt_asset_selection
from dbt.exceptions import EventCompilationError


log = get_dagster_logger()

THIS_DIR = Path(__file__).parent
DBT_ROOT = THIS_DIR.parent.joinpath('warehouse').absolute()
DBT_PROFILE_DIR = DBT_ROOT.joinpath('config').absolute()
DBT_TARGET_DIR = DBT_ROOT.joinpath('target').absolute()
DBT_MANIFEST_FILE = DBT_TARGET_DIR.joinpath('manifest.json').absolute()
DBT_TARGET = os.getenv('DBT_TARGET') or 'dev'


DEFAULT_TIMEZONE = 'Asia/Shanghai'


def _resource_factory():
    dbt = DbtCliResource(
        project_dir=str(DBT_ROOT),
        profiles_dir=str(DBT_PROFILE_DIR),
        target=DBT_TARGET,
    )
    return dbt


def init_manifest() -> Path:
    # 初始化dbt manifest.json文件
    dbt = _resource_factory()
    dbt.cli(
        ["parse"],
        target_path=DBT_TARGET_DIR
    ).wait()
    return DBT_MANIFEST_FILE


@dbt_assets(manifest=init_manifest())
def warehouse_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    # 载入dbt assets
    yield from dbt.cli(["build"], context=context).stream()


all_assets = [
    warehouse_assets,
]


def build_dbt_schedule_from_tag(
        assets,
        job_name: str,
        cron_schedule: str,
        dbt_select_tag: str,
        execution_timezone: Optional[str] = None,
        default_status: Optional[DefaultScheduleStatus] = DefaultScheduleStatus.STOPPED,
        **kwargs) -> Optional[ScheduleDefinition]:
    selection = build_dbt_asset_selection(assets, dbt_select=dbt_select_tag)
    try:
        keys = selection.resolve(assets)
        if len(keys) > 0:
            retval = ScheduleDefinition(
                name=job_name,
                cron_schedule=cron_schedule,
                job=define_asset_job(
                    name=job_name,
                    selection=selection,
                    config=kwargs.get('job_config', None),
                    tags=kwargs.get('job_tags', None),
                ),
                execution_timezone=execution_timezone,
                default_status=default_status,
            )
            return retval
    except EventCompilationError:
        return None


def _init_builtin_schedules() -> List[ScheduleDefinition]:
    daily_builds = build_dbt_schedule_from_tag(
        [warehouse_assets],
        "daily_build",
        "0 1 * * *",
        "tag:daily",
        DEFAULT_TIMEZONE,
        DefaultScheduleStatus.RUNNING,
    )
    weekly_build = build_dbt_schedule_from_tag(
        [warehouse_assets],
        "weekly_build",
        "0 1 * * 1",
        "tag:weekly",
        DEFAULT_TIMEZONE,
        DefaultScheduleStatus.RUNNING,
    )
    monthly_build = build_dbt_schedule_from_tag(
        [warehouse_assets],
        "monthly_build",
        "0 1 1 * *",
        "tag:monthly",
        DEFAULT_TIMEZONE,
        DefaultScheduleStatus.RUNNING,
    )
    builtin_schedules = []
    if daily_builds:
        builtin_schedules.append(daily_builds)
    if weekly_build:
        builtin_schedules.append(weekly_build)
    if monthly_build:
        builtin_schedules.append(monthly_build)
    return builtin_schedules


all_schedules = []

all_schedules += _init_builtin_schedules()

definition = Definitions(
    assets=all_assets,
    schedules=all_schedules,
    resources={
        "dbt": _resource_factory(),
    },
)
