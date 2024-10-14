from utils.sql.event_ingestion import ingest_data
from utils.sql.reports import create_reports
from utils.aws.aws_functions import get_daily_data, upload_reports
from config.config import data_folder, reports_folder, folder_alias
from os import getcwd

import datetime

if __name__ == "__main__":
    TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
    working_dir = getcwd()

    get_daily_data(
        download_from=f"{data_folder}/platform_transactions.csv",
        download_to=f"{working_dir}/platform_transactions.csv",
    )

    ingest_data()
    create_reports()

    upload_reports(
        upload_from=f"{data_folder}/finance_report.csv",
        upload_to=f"{reports_folder}/{folder_alias}/finance_report_{TODAY}.csv",
    )
    upload_reports(
        upload_from=f"{data_folder}/marketing_report.csv",
        upload_to=f"{reports_folder}/{folder_alias}/marketing_report_{TODAY}.csv",
    )

# 1. Download to Data Lake S3
# 2. Upload to PostgresSQL (With transformation customer_country and gender fill NA)
# 3. Run SQL Query for aggregation
# 4. Upload to S3

# Security, Cost, Reliability, Operateability, Performance, Scalability
# Observations
# Security Issues
# - Configs are uploaded in the repository (Vulnerable to hackers, anyone who has access to the prod configs can access the production data.
# - PII Data Exposure
# - Data Governance / User Access Control

# Reliability Issues
# - Unit Tests and Data Quality Tests
# - Debugging / Testing in Prod
# - Monitoring
# - CICD (IAC)

# Scalability Issues
# - PostgreSQL is for OLTP
# - Pandas is meant only for small amount of data - transformation can be sliced into chunks so memory can be utilized efficiently or you can use vectorization for more optimal transformation
#   Or use an OLAP tool and utilize its compute power
# - Orchestrator
# - File Format can be Parquet

# Operability
# - Hard to test because the supposed function parameters for reports and ingest are stored in config
# -

# Performance
