import json
import os

import boto3
from dotenv import load_dotenv


class BaseConfig:
    folder_alias = "CANEDA_MR"
    reports_folder = "reports"
    data_folder = "data"
    snowflake_table_name = "events"
    slack_alert_channel = "#etl-alert"
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

    @classmethod
    def get_secrets(cls, env: str) -> dict:
        if env == "dev":
            load_dotenv()
            return dict(os.environ)

        else:
            region_name = "ap-southeast-2"
            session = boto3.session.Session()
            client = session.client(service_name="secretsmanager", region_name=region_name)
            response = client.get_secret_value(
                SecretId=f"ae_exam_secrets_{env}",
            )
            return json.loads(response["SecretString"])


class ProdConfig(BaseConfig):
    def __init__(self):
        self.env = "dev"
        secrets = self.get_secrets(env=self.env)
        self.snowflake_account = secrets.get("snowflake-account")
        self.snowflake_user = secrets.get("snowflake-user")
        self.snowflake_password = secrets.get("snowflake-password")
        self.snowflake_database = "PLATFORM_PROD"
        self.snowflake_schema = "RAW"
        self.snowflake_wh = "EXAM_WH_PROD"
        self.bucket_name = "mark-data-analytics-bucket-prod"
        self.aws_key_id = secrets.get("aws-key-id")
        self.aws_secret_key = secrets.get("aws-secret-key")
        self.snowflake_role = "TRANSFORM_PROD"
        self.slack_token = secrets.get("slack-dagster-etl-bot-token")
        self.dagster_webserver_url = "http://127.0.0.1:3000/"


class StageConfig(BaseConfig):
    def __init__(self):
        self.env = "stage"
        secrets = self.get_secrets(env=self.env)
        self.snowflake_account = secrets.get("snowflake-account")
        self.snowflake_user = secrets.get("snowflake-user")
        self.snowflake_password = secrets.get("snowflake-password")
        self.snowflake_database = "PLATFORM_STAGE"
        self.snowflake_schema = "RAW"
        self.snowflake_wh = "EXAM_WH_STAGE"
        self.bucket_name = "mark-data-analytics-bucket-stage"
        self.aws_key_id = secrets.get("aws-key-id")
        self.aws_secret_key = secrets.get("aws-secret-key")
        self.snowflake_role = "TRANSFORM_STAGE"
        self.slack_token = secrets.get("slack-dagster-etl-bot-token")
        self.dagster_webserver_url = "http://127.0.0.1:3000/"


class DevConfig(BaseConfig):
    def __init__(self):
        self.env = "dev"
        secrets = self.get_secrets(env=self.env)
        self.snowflake_account = secrets.get("SNOWFLAKE_ACCOUNT")
        self.snowflake_user = secrets.get("SNOWFLAKE_USER")
        self.snowflake_password = secrets.get("SNOWFLAKE_PASSWORD")
        self.snowflake_database = "PLATFORM_DEV"
        self.snowflake_schema = "RAW"
        self.snowflake_wh = "EXAM_WH_DEV"
        self.bucket_name = "mark-data-analytics-bucket-dev"
        self.aws_key_id = secrets.get("AWS_KEY_ID")
        self.aws_secret_key = secrets.get("AWS_SECRET_KEY")
        self.snowflake_role = "TRANSFORM_DEV"
        self.slack_token = secrets.get("SLACK_DAGSTER_ETL_BOT_TOKEN")
        self.dagster_webserver_url = "http://127.0.0.1:3000/"


ENV_CONFIGS = {"dev": DevConfig(), "stage": StageConfig(), "prod": ProdConfig()}
