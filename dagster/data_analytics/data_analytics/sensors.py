from typing import Union

from dagster import SensorDefinition
from dagster_slack import make_slack_on_run_failure_sensor

from .config.config import ProdConfig, DevConfig, StageConfig


def make_slack_on_failure_sensor(env_config: Union[ProdConfig, DevConfig, StageConfig]) -> SensorDefinition:
    return make_slack_on_run_failure_sensor(
        channel=env_config.slack_alert_channel, slack_token=env_config.slack_token, webserver_base_url=env_config.dagster_webserver_url
    )
