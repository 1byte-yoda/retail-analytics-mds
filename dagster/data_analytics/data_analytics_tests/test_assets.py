import io
from datetime import datetime
from decimal import Decimal

import boto3
import pandas as pd
from dagster import materialize
from pandas.testing import assert_frame_equal

from ..data_analytics.assets.platform_events import events_table
from ..data_analytics.assets.ae_exam import s3_file_report_stage, finance_report_file, marketing_report_file, ae_exam_dbt_assets


def test_s3_file_report_stage(fake_asset_context):
    s3_file_report_stage(context=fake_asset_context)
    with fake_asset_context.resources.snowflake.get_connection() as conn:
        check_stage_exist_query = f"""
            SELECT 1
            FROM INFORMATION_SCHEMA.STAGES
            WHERE STAGE_SCHEMA = '{conn.schema}'
                AND STAGE_NAME = 'EVENTS_STAGE'
                AND STAGE_CATALOG = '{conn.database}'
        """
        check_rows = conn.cursor().execute(check_stage_exist_query).fetchall()
        assert len(check_rows) > 0


def test_events_table_asset(fake_asset_context):
    events_table(context=fake_asset_context)

    with fake_asset_context.resources.snowflake.get_connection() as conn:
        check_table_exist_query = f"""
            SELECT 1
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = '{conn.schema}'
                AND TABLE_NAME = 'EVENTS'
                AND TABLE_CATALOG = '{conn.database}'
        """
        check_table_populated_query = f'SELECT COUNT(1) FROM "{conn.database}"."{conn.schema}".EVENTS'
        print(check_table_exist_query)
        print(check_table_populated_query)
        check_table_rows = conn.cursor().execute(check_table_exist_query).fetchall()
        events_table_rows = conn.cursor().execute(check_table_populated_query).fetchall()
        assert len(check_table_rows) == 1
        assert events_table_rows[0][0] > 0


def test_ae_exam_dbt(fake_resources):
    result = materialize(assets=[ae_exam_dbt_assets], resources=fake_resources)
    assert result.success


def test_finance_report_file(fake_asset_context):
    finance_report_file(context=fake_asset_context)
    env_config = fake_asset_context.resources.env_config
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"{env_config.reports_folder}/{env_config.folder_alias}/finance_report_{today}_0_0_0.snappy.parquet"

    client = boto3.client("s3")
    response = client.get_object(Bucket=env_config.bucket_name, Key=file_path)
    df = pd.read_parquet(io.BytesIO(response["Body"].read()))
    expected_df = pd.DataFrame.from_dict(
        {
            "CUSTOMER_COUNTRY": ["Australia", "Brazil", "Not Available", "Philippines", "United States"],
            "TOTAL_VALUE": [36.07, 4512.82, 1733.4, 5644.28, 2603.88],
        }
    )
    assert_frame_equal(df.sort_values(by="CUSTOMER_COUNTRY", ignore_index=True), expected_df)


def test_marketing_report_file(fake_asset_context):
    marketing_report_file(context=fake_asset_context)
    env_config = fake_asset_context.resources.env_config
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"{env_config.reports_folder}/{env_config.folder_alias}/marketing_report_{today}_0_0_0.snappy.parquet"

    client = boto3.client("s3")
    response = client.get_object(Bucket=env_config.bucket_name, Key=file_path)
    df = pd.read_parquet(io.BytesIO(response["Body"].read()))
    expected_df = pd.DataFrame.from_dict(
        {
            "CUSTOMER_COUNTRY": ["Australia", "Brazil", "Not Available", "Philippines", "United States"],
            "TOTAL_TRANSACTIONS": [Decimal("2"), Decimal("314"), Decimal("123"), Decimal("382"), Decimal("179")],
        }
    )
    assert_frame_equal(
        df.sort_values(by="CUSTOMER_COUNTRY", ignore_index=True),
        expected_df,
    )
