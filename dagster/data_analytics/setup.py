from setuptools import find_packages, setup

setup(
    name="data_analytics",
    packages=find_packages(exclude=["data_analytics_tests"]),
    install_requires=["dagster", "dagster-cloud"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
