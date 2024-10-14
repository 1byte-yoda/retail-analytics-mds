import boto3
from config.config import bucket_name

def get_daily_data(download_from, download_to):
    """
    Get daily data from S3 bucket
    """
    s3_client = boto3.client("s3")

    s3_client.download_file(
        Bucket=bucket_name, Key=download_from, Filename=download_to
    )


def upload_reports(upload_from, upload_to):
    """
    Upload reports to S3 bucket
    """
    s3_client = boto3.client("s3")

    s3_client.upload_file(
        Bucket=bucket_name, Filename=upload_from, Key=upload_to
    )
