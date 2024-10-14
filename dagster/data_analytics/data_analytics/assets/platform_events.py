import datetime

from dagster import asset, op, OpExecutionContext, RetryPolicy, graph_asset, AssetExecutionContext, In, Nothing


@op(retry_policy=RetryPolicy(max_retries=3), required_resource_keys={"snowflake"}, ins={"start": In(Nothing)})
def create_events_table(context: OpExecutionContext) -> str:
    """Generates the events_table using csv files from platform_transactions in S3"""
    database = "PLATFORM_DEV"
    table_name = "events"
    datatypes = {
        "transaction_id": "INT",
        "purchase_price": "FLOAT",
        "product_value": "FLOAT",
        "product_name": "VARCHAR(255)",
        "first_name": "VARCHAR(255)",
        "last_name": "VARCHAR(255)",
        "email": "VARCHAR(255)",
        "gender": "VARCHAR(255)",
        "customer_country": "VARCHAR(255)",
        "client_country": "VARCHAR(255)",
    }
    column_definition = ",\n".join(
        f"{column_name} {column_type}" for column_name, column_type in datatypes.items()
    )

    create_table_sql = f'CREATE TABLE IF NOT EXISTS "{database}"."RAW".{table_name} ({column_definition})'
    context.resources.snowflake.execute_query(create_table_sql)
    context.log.info("Table created successfully.")
    return table_name


@op(retry_policy=RetryPolicy(max_retries=3), required_resource_keys={"snowflake"})
def create_s3_file_stage(context: OpExecutionContext, table_name: str) -> str:
    """Creates a Snowflake Stage object using the S3 platform_transactions file"""
    bucket_name = "ae-exam-bucket-dev"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    database = "PLATFORM_DEV"
    stage = f"{table_name}_stage"
    s3_path = f"s3://{bucket_name}/data/{date}/"

    query = f"""CREATE OR REPLACE STAGE "{database}"."RAW".{stage}
    URL='{s3_path}'
    CREDENTIALS=(AWS_KEY_ID='<AWS_KEY_ID_HERE>' AWS_SECRET_KEY='<AWS_SECRET_KEY_HERE>');"""
    context.resources.snowflake.execute_query(query)
    context.log.info("Stage created successfully.")
    return s3_path


@graph_asset
def s3_csv_snowflake_stage() -> None:
    """Creates a Snowflake Stage object using the S3 platform_transactions file"""
    table_name = create_events_table()
    s3_path = create_s3_file_stage(table_name)
    return s3_path


@asset(deps=[s3_csv_snowflake_stage], required_resource_keys={"snowflake"})
def events_table(context: AssetExecutionContext) -> None:
    """Creates the events table using the platform_transactions.csv via Snowflake Stage"""
    database = "PLATFORM_DEV"
    table_name = "events"
    stage = "events_stage"
    query = f"""
    COPY INTO "{database}".RAW.{table_name}
    FROM @"{database}".RAW.{stage}
    FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);
    """
    context.resources.snowflake.execute_query(query)
    context.log.info("File in Stage was Loaded Successfully.")
    return


@asset(deps=[events_table])
def just_another_asset() -> str:
    return "Hello World"