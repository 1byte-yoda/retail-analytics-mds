import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    folder_alias = "CANEDA_MR"
    reports_folder = "reports"
    data_folder = "data"
    snowflake_table_name = "events"
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


class ProdConfig(BaseConfig):
    snowflake_account = os.environ.get("SNOWFLAKE_ACCOUNT")
    snowflake_user = os.environ.get("SNOWFLAKE_USER")
    snowflake_password = os.environ.get("SNOWFLAKE_PASSWORD")
    snowflake_database = "PLATFORM_PROD"
    snowflake_schema = "RAW"
    snowflake_wh = "EXAM_WH_PROD"
    bucket_name = "ae-exam-bucket-prod"
    aws_key_id = os.environ.get("AWS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_KEY")
    snowflake_role = "TRANSFORM_PROD"


class StageConfig(BaseConfig):
    snowflake_account = os.environ.get("SNOWFLAKE_ACCOUNT")
    snowflake_user = os.environ.get("SNOWFLAKE_USER")
    snowflake_password = os.environ.get("SNOWFLAKE_PASSWORD")
    snowflake_database = "PLATFORM_STAGE"
    snowflake_schema = "RAW"
    snowflake_wh = "EXAM_WH_STAGE"
    bucket_name = "ae-exam-bucket-stage"
    aws_key_id = os.environ.get("AWS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_KEY")
    snowflake_role = "TRANSFORM_STAGE"


class DevConfig(BaseConfig):
    snowflake_account = os.environ.get("SNOWFLAKE_ACCOUNT")
    snowflake_user = os.environ.get("SNOWFLAKE_USER")
    snowflake_password = os.environ.get("SNOWFLAKE_PASSWORD")
    snowflake_database = "PLATFORM_DEV"
    snowflake_schema = "RAW"
    snowflake_wh = "EXAM_WH_DEV"
    bucket_name = "ae-exam-bucket-dev"
    aws_key_id = os.environ.get("AWS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_KEY")
    snowflake_role = "TRANSFORM_DEV"


ENV_CONFIGS = {
    "dev": DevConfig(),
    "stage": StageConfig(),
    "prod": ProdConfig()
}
