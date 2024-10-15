import json
import os
import sys

import boto3
from dotenv import load_dotenv


def create_secrets_from_env(env: str):
    load_dotenv(dotenv_path=f"env_examples/.env.{env}")


    secret_keys = [
        "SLACK_DAGSTER_ETL_BOT_TOKEN",
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "AWS_KEY_ID",
        "AWS_SECRET_KEY",
        "TERRAFORM_TOKEN"
    ]

    secrets = {}

    for sk in secret_keys:
        secret_val = os.environ.get(sk)
        if not secret_val:
            print(f"Secret {sk} was not found in the Secret Manager")

        if env == "dev":
            secrets[sk] = secret_val

        else:
            secret_name = sk.replace("_", "-").lower()
            secrets[secret_name] = secret_val

    return secrets


def write_secrets(secrets: dict, env: str):
    if env == "dev":
        secret = ""
        for sk, sv in secrets.items():
            secret += f"{sk}={sv}\n"

        with open(f"dagster/data_analytics/.env", "w") as f:
            f.write(secret)
    else:
        region_name = "ap-southeast-2"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        response = client.create_secret(
            Name=f"ae_exam_secrets_{env}",
            SecretString=json.dumps(secrets),
        )
        print(response)


if __name__ == '__main__':
    env = sys.argv[1]
    secrets = create_secrets_from_env(env=env)
    write_secrets(secrets=secrets, env=env)