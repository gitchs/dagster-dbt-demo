#!/usr/bin/env python3
import os
import time
from pathlib import Path
from dagster import asset
from dagster import get_dagster_logger
from dagster import Definitions
from dagster import MaterializeResult
from dagster import AssetExecutionContext
from dagster import DefaultScheduleStatus
from dagster_dbt import DbtCliResource
from dagster_dbt import dbt_assets
from dagster_dbt import build_schedule_from_dbt_selection

log = get_dagster_logger()

THIS_DIR = Path(__file__).parent
DBT_ROOT = THIS_DIR.parent.joinpath('warehouse').absolute()
DBT_PROFILE_DIR = DBT_ROOT.joinpath('config').absolute()
DBT_TARGET_DIR = DBT_ROOT.joinpath('target').absolute()
DBT_MANIFEST_FILE = DBT_TARGET_DIR.joinpath('manifest.json').absolute()
DBT_TARGET = os.getenv('DBT_TARGET') or 'dev'


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


@asset(
    name="dbt_docs_generate",
    description="执行dbt docs generate，更新文档",
    compute_kind="python"
)
def dbt_docs_generate(context: AssetExecutionContext):
    dbt = _resource_factory()
    start = time.time()
    dbt.cli(['docs', 'generate']).wait()
    duration = time.time() - start
    return MaterializeResult(
        metadata={
            'Execution Duration(s)': duration
        },
    )


all_assets = [
    dbt_docs_generate,
    warehouse_assets,
]


dbt_daily_schedule = build_schedule_from_dbt_selection(
    [warehouse_assets],
    job_name="dbt_daily_materialized",
    cron_schedule="0 1 * * *",  # At 01:00 everyday
    dbt_select="tag:daily",     # 根据tag选择dbt模型
    default_status=DefaultScheduleStatus.RUNNING,
    execution_timezone='Asia/Shanghai',  # 根据需要设置时区
)


all_schedules = [
    dbt_daily_schedule,
]

definition = Definitions(
    assets=all_assets,
    schedules=all_schedules,
    resources={
        "dbt": _resource_factory(),
    },
)

