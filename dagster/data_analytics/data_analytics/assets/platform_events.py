import datetime

from dagster import asset, AssetExecutionContext


@asset(required_resource_keys={"snowflake", "env_config"})
def events_table(context: AssetExecutionContext) -> None:
    """Creates the events table using the platform_transactions.csv via Snowflake Stage"""
    env_config = context.resources.env_config
    table_name = f'"{env_config.snowflake_database}"."{env_config.snowflake_schema}".{env_config.snowflake_table_name}'
    stage_name = f'"{env_config.snowflake_database}"."{env_config.snowflake_schema}".{env_config.snowflake_table_name}_stage'
    column_definition = ",\n".join(f"{column_name} {column_type}" for column_name, column_type in env_config.datatypes.items())
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    create_table_sql = f"CREATE TABLE IF NOT EXISTS table_name ({column_definition})"
    create_stage_sql = f"""
        CREATE OR REPLACE STAGE stage_name
        URL='s3://{env_config.bucket_name}/{env_config.data_folder}/{date}/'
        CREDENTIALS=(AWS_KEY_ID='{env_config.aws_key_id}' AWS_SECRET_KEY='{env_config.aws_secret_key}');
    """
    copy_file_sql = f"""
        COPY INTO {table_name}
        FROM @{stage_name}
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1)
    """

    with context.resources.snowflake.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        cursor.execute(create_stage_sql)
        cursor.execute(copy_file_sql)
        conn.commit()

    context.log.info(f"{table_name} was populated successfully")
    return
