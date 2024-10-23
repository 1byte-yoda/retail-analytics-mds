import datetime
from typing import Mapping, Any

from dagster import AssetKey, AssetExecutionContext
from dagster_dbt import DagsterDbtTranslator, dbt_assets
from dagster import asset

from ..project import dbt_project


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return AssetKey(f"{name}_table")
        else:
            return super().get_asset_key(dbt_resource_props)


@dbt_assets(manifest=dbt_project.manifest_path, dagster_dbt_translator=CustomDagsterDbtTranslator(), required_resource_keys={"env_config", "dbt"})
def data_analytics_dbt_assets(
    context: AssetExecutionContext,
):
    if context.resources.env_config.env == "dev":
        profiles_arg = ["--profiles-dir", "~/.dbt"]
        args = (["compile", *profiles_arg], ["build", *profiles_arg])
    else:
        args = (["compile"], ["build"])
    yield from context.resources.dbt.cli(args[0], context=context).stream()
    yield from context.resources.dbt.cli(args[1], context=context).stream()


@asset(deps=["finance_report", "marketing_report"], required_resource_keys={"snowflake", "env_config"})
def s3_file_report_stage(context: AssetExecutionContext) -> None:
    """Snowflake Stage Object for S3 Report Dumps"""
    env_config = context.resources.env_config
    schema = "REPORT"
    s3_bucket = f"'s3://{env_config.bucket_name}/{env_config.reports_folder}/{env_config.folder_alias}/'"
    stage = f'"{env_config.snowflake_database}"."{schema}".report_stage'

    query = f"""
        CREATE OR REPLACE STAGE {stage}
        URL = {s3_bucket}
        FILE_FORMAT = (TYPE = PARQUET)
        CREDENTIALS = (AWS_KEY_ID='{env_config.aws_key_id}' AWS_SECRET_KEY='{env_config.aws_secret_key}');
    """
    context.resources.snowflake.execute_query(query)


def _get_report_file_copy_query(table_name: str, database: str) -> str:
    schema = "REPORT"
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    query = f"""
        COPY INTO @"{database}"."{schema}".report_stage/{table_name}_{today}
        FROM "{database}".{schema}.{table_name}
        OVERWRITE = TRUE HEADER = TRUE
    """
    return query


@asset(deps=[s3_file_report_stage], required_resource_keys={"snowflake", "env_config"})
def finance_report_file(context: AssetExecutionContext) -> None:
    """Data Mart Report for Finance Team in Parquet File Format"""
    copy_file_query = _get_report_file_copy_query(table_name="finance_report", database=context.resources.env_config.snowflake_database)
    context.resources.snowflake.execute_query(copy_file_query)
    context.log.info("Finance Report File Unloaded Successfully")


@asset(deps=[s3_file_report_stage], required_resource_keys={"snowflake", "env_config"})
def marketing_report_file(context: AssetExecutionContext) -> None:
    """Data Mart Report for Marketing Team in Parquet File Format"""
    copy_file_query = _get_report_file_copy_query(table_name="marketing_report", database=context.resources.env_config.snowflake_database)
    context.resources.snowflake.execute_query(copy_file_query)
    context.log.info("Marketing Report File Unloaded Successfully")
