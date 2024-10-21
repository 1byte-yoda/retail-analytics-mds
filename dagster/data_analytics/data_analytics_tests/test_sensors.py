from dagster import repository

from ..data_analytics.config.config import ENV_CONFIGS
from ..data_analytics.sensors import make_slack_on_failure_sensor


def test_slack_on_failure_def():
    @repository
    def my_repo_local():
        return [make_slack_on_failure_sensor(env_config=ENV_CONFIGS["dev"])]

    @repository
    def my_repo_staging():
        return [make_slack_on_failure_sensor(env_config=ENV_CONFIGS["stage"])]

    @repository
    def my_repo_prod():
        return [make_slack_on_failure_sensor(env_config=ENV_CONFIGS["prod"])]

    assert my_repo_local.has_sensor_def("slack_on_run_failure")
    assert my_repo_staging.has_sensor_def("slack_on_run_failure")
    assert my_repo_prod.has_sensor_def("slack_on_run_failure")
