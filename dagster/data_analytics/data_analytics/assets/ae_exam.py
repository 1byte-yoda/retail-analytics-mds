import datetime
from typing import Mapping, Any, Union

from dagster import AssetKey, AssetExecutionContext, asset_check, AssetCheckExecutionContext, AssetCheckResult, AssetCheckSeverity, op
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets
from dagster import asset

from ..config.config import ProdConfig, DevConfig, StageConfig
from ..project import dbt_project


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return AssetKey(f"{name}_table")
        else:
            return super().get_asset_key(dbt_resource_props)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
    required_resource_keys={"env_config", "dbt"}
)
def ae_exam_dbt_assets(context: AssetExecutionContext, ):
    if context.resources.env_config.env == "dev":
        args = ["build", "--profiles-dir", "~/.dbt"]
    else:
        args = ["build"]
    yield from context.resources.dbt.cli(args, context=context).stream()

@asset(deps=["finance_report", "marketing_report"], required_resource_keys={"snowflake", "env_config"})
def s3_file_report_stage(context) -> None:
    env_config = context.resources.env_config
    database = env_config.snowflake_database
    schema = "REPORT"
    bucket_name = env_config.bucket_name
    reports_folder = env_config.reports_folder
    folder_alias = env_config.folder_alias
    stage = "report_stage"

    query = f"""
        CREATE OR REPLACE STAGE "{database}"."{schema}".{stage}
        URL = 's3://{bucket_name}/{reports_folder}/{folder_alias}/'
        FILE_FORMAT = (TYPE = PARQUET)
        CREDENTIALS = (AWS_KEY_ID='{env_config.aws_key_id}' AWS_SECRET_KEY='{env_config.aws_secret_key}');
    """
    context.resources.snowflake.execute_query(query)


@asset(deps=["s3_file_report_stage"], required_resource_keys={"snowflake", "env_config"})
def finance_report_file(context: AssetExecutionContext) -> None :
    env_config = context.resources.env_config
    database = env_config.snowflake_database
    table_name = "finance_report"
    schema = "REPORT"
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    query = f"""
        COPY INTO @"{database}"."{schema}".report_stage/finance_report_{today}
        FROM "{database}".{schema}.{table_name}
        OVERWRITE = TRUE HEADER = TRUE
    """
    context.resources.snowflake.execute_query(query)
    context.log.info("Finance Report File Unloaded Successfully")


@asset(deps=["s3_file_report_stage"], required_resource_keys={"snowflake", "env_config"})
def marketing_report_file(context: AssetExecutionContext) -> None :
    env_config = context.resources.env_config
    database = env_config.snowflake_database
    table_name = "marketing_report"
    schema = "REPORT"
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    query = f"""
        COPY INTO @"{database}"."{schema}".report_stage/marketing_report_{today}
        FROM "{database}".{schema}.{table_name}
        OVERWRITE = TRUE HEADER = TRUE
    """
    context.resources.snowflake.execute_query(query)
    context.log.info("Marketing Report File Unloaded Successfully")