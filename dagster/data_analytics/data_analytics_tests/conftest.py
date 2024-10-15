import os

import pytest
from dagster import build_op_context, build_asset_context
from dagster_dbt import DbtCliResource
from dagster_snowflake import SnowflakeResource

from ..data_analytics.config.config import ENV_CONFIGS
from ..data_analytics.project import dbt_project


@pytest.fixture
def fake_op_context(fake_resources):
    yield build_op_context(resources=fake_resources)


@pytest.fixture
def fake_resources():
    env = os.environ.get("ENV")
    env_config = ENV_CONFIGS[env]
    dbt_dev_resource = DbtCliResource(
        project_dir=dbt_project,
        target=env,
    )
    snowflake = SnowflakeResource(
        account=env_config.snowflake_account,
        user=env_config.snowflake_user,
        password=env_config.snowflake_password,
        database=env_config.snowflake_database,
        schema=env_config.snowflake_schema,
        warehouse=env_config.snowflake_wh,
        role=env_config.snowflake_role,
    )
    yield {"env_config": env_config, "snowflake": snowflake, "dbt": dbt_dev_resource}


@pytest.fixture
def fake_asset_context(fake_resources):
    yield build_asset_context(resources=fake_resources)
