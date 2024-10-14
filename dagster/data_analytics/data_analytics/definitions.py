from dagster import Definitions, load_assets_from_modules
from dagster_snowflake import SnowflakeResource

from .assets import platform_events

all_assets = load_assets_from_modules([platform_events])

snowflake_io_manager = SnowflakeResource(
    account="rnpvpsy-pr83548",
    user="dbt_dev",
    password="dbtPassword123",
    database="PLATFORM_DEV",
    schema="RAW",
    warehouse="EXAM_WH_DEV",
)

defs = Definitions(
    assets=all_assets,
    resources={"snowflake": snowflake_io_manager}
    # jobs=[platform_events.ingest_events_table]
)
