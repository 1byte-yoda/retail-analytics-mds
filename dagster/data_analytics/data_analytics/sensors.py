import os

from dagster import SensorDefinition, EnvVar
from dagster_slack import make_slack_on_run_failure_sensor


def make_slack_on_failure_sensor() -> SensorDefinition:
    return make_slack_on_run_failure_sensor(
        channel="#etl-alert",
        slack_token=EnvVar("SLACK_DAGSTER_ETL_BOT_TOKEN"),
        webserver_base_url="http://127.0.0.1:3000/"
    )