#!/usr/bin/env python3
from pathlib import Path
from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_dbt import load_assets_from_dbt_project
from dagster_dbt import DagsterDbtTranslator


THIS_DIR = Path(__file__).parent
DBT_ROOT = THIS_DIR.parent.joinpath('warehouse').absolute()
DBT_PROFILE_DIR = DBT_ROOT.joinpath('config')


class CustomTranslator(DagsterDbtTranslator):
    pass


dbt_assets = load_assets_from_dbt_project(
    str(DBT_ROOT),
    profiles_dir=str(DBT_PROFILE_DIR),
    dagster_dbt_translator=CustomTranslator(),
)


all_assets = dbt_assets


defs = Definitions(
    assets=all_assets,
    resources={
        "dbt": DbtCliResource(project_dir=str(DBT_ROOT)),
    },
)

