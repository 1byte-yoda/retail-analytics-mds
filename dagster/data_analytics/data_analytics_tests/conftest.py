import os
from datetime import datetime
from uuid import uuid4

import boto3
import pytest
from dagster import build_op_context, build_asset_context
from dagster_dbt import DbtCliResource
from dagster_snowflake import SnowflakeResource

from ..data_analytics.config.config import ENV_CONFIGS
from ..data_analytics.project import dbt_project, get_project_root


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown(fake_resources):
    bucket_name = "ae-exam-bucket-stage"
    _upload_test_file_to_s3(bucket_name=bucket_name)
    yield
    _delete_s3_folder(bucket_name=bucket_name, folder="data/")
    _delete_s3_folder(bucket_name=bucket_name, folder="reports/")
    _drop_dimensional_tables(fake_resources=fake_resources)


@pytest.fixture(scope="session")
def fake_op_context(fake_resources):
    yield build_op_context(resources=fake_resources)


@pytest.fixture(scope="session")
def fake_resources():
    env = os.environ.get("ENV")
    env_config = ENV_CONFIGS[env]
    dbt_dev_resource = DbtCliResource(
        project_dir=dbt_project,
        target=env,
    )
    snowflake = SnowflakeResource(
        account=env_config.snowflake_account,
        user=env_config.snowflake_user,
        password=env_config.snowflake_password,
        database=env_config.snowflake_database,
        schema=env_config.snowflake_schema,
        warehouse=env_config.snowflake_wh,
        role=env_config.snowflake_role,
    )
    yield {"env_config": env_config, "snowflake": snowflake, "dbt": dbt_dev_resource}


@pytest.fixture(scope="session")
def fake_asset_context(fake_resources):
    yield build_asset_context(resources=fake_resources)


def _upload_test_file_to_s3(bucket_name: str):
    today = datetime.today().date()
    s3_key = f"data/{today}/platform_transactions_{uuid4().hex}.csv"
    test_file_path = get_project_root() / "data" / "platform_transactions.csv"
    s3_client = boto3.client("s3")
    s3_client.upload_file(test_file_path, bucket_name, s3_key)

    print(f"File {test_file_path} was uploaded to bucket {bucket_name} with key {s3_key}")


def _delete_s3_folder(bucket_name: str, folder: str):
    s3_client = boto3.client("s3")
    continuation_token = None

    while True:
        list_kwargs = {"Bucket": bucket_name, "Prefix": folder}
        if continuation_token:
            list_kwargs["ContinuationToken"] = continuation_token

        response = s3_client.list_objects_v2(**list_kwargs)

        if "Contents" in response:
            delete_keys = [{"Key": obj["Key"]} for obj in response["Contents"]]
            s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": delete_keys})
            print(f"Deleted {len(delete_keys)} objects from data/")

        if response.get("IsTruncated"):
            continuation_token = response["NextContinuationToken"]
        else:
            break


def _drop_dimensional_tables(fake_resources: dict):
    with fake_resources.get("snowflake").get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE PLATFORM_STAGE.RAW.EVENTS;")
        cursor.execute("DROP TABLE PLATFORM_STAGE.RAW.RAW_EVENTS;")
        cursor.execute("DROP TABLE PLATFORM_STAGE.DIM.DIM_CUSTOMERS;")
        cursor.execute("DROP TABLE PLATFORM_STAGE.DIM.DIM_CLIENT_INFO;")
        cursor.execute("DROP TABLE PLATFORM_STAGE.DIM.DIM_PRODUCTS;")
        cursor.execute("DROP TABLE PLATFORM_STAGE.FACT.FACT_EVENTS;")
        cursor.execute("DROP TABLE PLATFORM_STAGE.REPORT.FINANCE_REPORT;")
        cursor.execute("DROP TABLE PLATFORM_STAGE.REPORT.MARKETING_REPORT;")
        conn.commit()
