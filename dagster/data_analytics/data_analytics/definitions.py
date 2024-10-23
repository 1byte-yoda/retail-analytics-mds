import os

from dagster import Definitions, load_assets_from_modules, ScheduleDefinition
from dagster_dbt import DbtCliResource
from dagster_snowflake import SnowflakeResource

from .assets import platform_events, data_analytics
from .jobs import indebted_data_analytics_job
from .project import dbt_project
from .sensors import make_slack_on_failure_sensor
from .config.config import ENV_CONFIGS


env: str = os.environ.get("ENV", "dev")
env_config = ENV_CONFIGS[env]

all_assets = load_assets_from_modules([platform_events, data_analytics])

snowflake = SnowflakeResource(
    account=env_config.snowflake_account,
    user=env_config.snowflake_user,
    password=env_config.snowflake_password,
    database=env_config.snowflake_database,
    schema=env_config.snowflake_schema,
    warehouse=env_config.snowflake_wh,
    role=env_config.snowflake_role,
)

dbt_dev_resource = DbtCliResource(
    project_dir=dbt_project,
    target=env,
)

indebted_ae_schedule = ScheduleDefinition(
    job=indebted_data_analytics_job,
    cron_schedule="0 1 * * *",  # every 1am UTC daily
)

defs = Definitions(
    assets=all_assets,
    resources={"snowflake": snowflake, "dbt": dbt_dev_resource, "env_config": env_config},
    jobs=[indebted_data_analytics_job],
    sensors=[make_slack_on_failure_sensor(env_config=env_config)],
    schedules=[indebted_ae_schedule],
)
