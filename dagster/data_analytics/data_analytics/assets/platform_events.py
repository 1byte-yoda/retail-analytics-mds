import datetime

from dagster import asset, op, OpExecutionContext, RetryPolicy, graph_asset, AssetExecutionContext, In, Nothing, asset_check, AssetCheckResult, AssetCheckSeverity, AssetCheckExecutionContext


@op(retry_policy=RetryPolicy(max_retries=3), required_resource_keys={"snowflake", "env_config"}, ins={"start": In(Nothing)})
def create_events_table(context: OpExecutionContext) -> str:
    """Generates the events table using csv files from platform_transactions in S3"""
    env_config = context.resources.env_config
    database = env_config.snowflake_database
    table_name = env_config.snowflake_table_name
    schema = env_config.snowflake_schema
    datatypes = env_config.datatypes
    column_definition = ",\n".join(
        f"{column_name} {column_type}" for column_name, column_type in datatypes.items()
    )

    create_table_sql = f'CREATE TABLE IF NOT EXISTS "{database}"."{schema}".{table_name} ({column_definition})'
    context.resources.snowflake.execute_query(create_table_sql)
    context.log.info("Table created successfully.")
    return table_name


@op(retry_policy=RetryPolicy(max_retries=3), required_resource_keys={"snowflake", "env_config"})
def create_s3_file_stage(context: OpExecutionContext, table_name: str) -> str:
    """Creates a Snowflake Stage object using the S3 platform_transactions file"""
    env_config = context.resources.env_config
    schema = env_config.snowflake_schema
    database = env_config.snowflake_database
    stage = f"{env_config.snowflake_table_name}_stage"
    bucket_name = env_config.bucket_name
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data_folder = env_config.data_folder
    s3_path = f"s3://{bucket_name}/{data_folder}/{date}/"

    query = f"""
        CREATE OR REPLACE STAGE "{database}"."{schema}".{stage}
        URL='{s3_path}'
        CREDENTIALS=(AWS_KEY_ID='{env_config.aws_key_id}' AWS_SECRET_KEY='{env_config.aws_secret_key}');
    """
    context.resources.snowflake.execute_query(query)
    context.log.info("Stage created successfully.")
    return s3_path


@graph_asset
def s3_csv_snowflake_stage() -> None:
    """Creates a Snowflake Stage object using the S3 platform_transactions file"""
    table_name = create_events_table()
    s3_path = create_s3_file_stage(table_name)
    return s3_path


@asset(deps=[s3_csv_snowflake_stage], required_resource_keys={"snowflake", "env_config"})
def events_table(context: AssetExecutionContext) -> None:
    """Creates the events table using the platform_transactions.csv via Snowflake Stage"""
    env_config = context.resources.env_config
    database = env_config.snowflake_database
    table_name = env_config.snowflake_table_name
    schema = env_config.snowflake_schema
    stage = f"{env_config.snowflake_table_name}_stage"

    query = f"""
        COPY INTO "{database}".{schema}.{table_name}
        FROM @"{database}".{schema}.{stage}
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);
    """
    context.resources.snowflake.execute_query(query)
    context.log.info("File in Stage was Loaded Successfully.")
    return
