import os

from dagster import Definitions, load_assets_from_modules, EnvVar
from dagster_dbt import DbtCliResource
from dagster_snowflake import SnowflakeResource

from .assets import platform_events, ae_exam
from .jobs import indebted_ae_exam_job
from .project import dbt_project
from .sensors import make_slack_on_failure_sensor
from .config.config import ENV_CONFIGS


env: str = os.environ.get("ENV", "dev")
env_config = ENV_CONFIGS[env]

all_assets = load_assets_from_modules([platform_events, ae_exam])

snowflake_io_manager = SnowflakeResource(
    account=env_config.snowflake_account,
    user=env_config.snowflake_user,
    password=env_config.snowflake_password,
    database=env_config.snowflake_database,
    schema=env_config.snowflake_schema,
    warehouse=env_config.snowflake_wh,
)

dbt_dev_resource = DbtCliResource(
    project_dir=dbt_project,
    target=env,
)

defs = Definitions(
    assets=all_assets,
    resources={
        "snowflake": snowflake_io_manager,
        "dbt": dbt_dev_resource,
        "env_config": env_config
    },
    jobs=[indebted_ae_exam_job],
    sensors=[make_slack_on_failure_sensor()]
)
