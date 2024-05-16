#!/usr/bin/env python3
import time
import random
import datetime
from dagster import asset
from dagster import get_dagster_logger
from dagster import Definitions
from dagster import DefaultScheduleStatus
from dagster import ScheduleDefinition
from dagster import MaterializeResult
from dagster import define_asset_job


log = get_dagster_logger()


@asset(group_name="example")
def task0():
    log.info('execute task0')


@asset(deps=[task0], group_name="example")
def task1():
    start = datetime.datetime.now()
    time.sleep(random.random() * 5)
    end = datetime.datetime.now()
    duration = (end - start).total_seconds()
    return MaterializeResult(
        metadata={
            "start": str(start),
            "end": str(end),
            "duration": duration
        }
    )


all_assets = [
    task0,
    task1
]

all_schedules = [
    ScheduleDefinition(
        name="daily_build",
        cron_schedule="0 1 * * *",
        default_status=DefaultScheduleStatus.RUNNING,
        job=define_asset_job(
            name="daily_build",
            selection=[task0, task1]
        ),
        execution_timezone='Asia/Shanghai'
    ),
]


definitions = Definitions(
    assets=all_assets,
    schedules=all_schedules,
)