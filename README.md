You just started working for a company that sells products for a couple of countries in the world.

The Data Engineering team set up a process where you will receive a file into an s3 bucket on a daily basis. (An example of the last one is available under the ```data/``` folder).

On AWS S3, the file will be under the following folder:

```data/platform_transactions.csv```

After transformation, the files will be loaded into the S3 buckets `reports` folder.

This repository should contain a framework to:

- Grab the data from an s3 bucket
- Clean/transform the data
- Ingest into a Data Lake
- Create 2 reports
  - Total value of transactions and send to the Finance Team (```reports/``` folder inside the AWS S3 bucket)
  - Total number of transactions and sent to the Marketing Team (```reports/``` folder inside the AWS S3 bucket)

Details:

- Our Data Lake details are set up in the config folder (There are 3 environments, dev, stage and prod, but only prod is on the script)
- The Data Lake only contains 1 database, 1 schema, and 1 table inside it. All are defined inside the config folder too.
- At the moment, only 2 reports are created, one for the Finance Team and another one for the Marketing Team

You arrive on your first day at the job and see this repository. In the current state, the scripts work, it can manage all tasks required.
But there are new clients and products that will be added to the company soon, and more teams will request new reports, what would you do?

Would you change the current state of the repository or not? If you decide to do some changes, fork this repo and share with us!

----
**IMPORTANT**: <br>
Before doing anything else, in `config.py`, rename the `folder_alias` variable to your `LASTNAME_initials` (ex. `DELACRUZ_J`, `SMITH_S`)

#
# 1. Install Terraform
# 2. Create a .env file and copy the content from .env.example file 
# 3. Create a snowflake account and save your credentials (Account ID, Username, Password, Role)
# 4. Replace each Snowflake Related Values in the .env file using the snowflake credentials from step 3
# 5. Create a terraform cloud account
# 6. In terraform cloud, create an Organization Token and save it in the .env file
# User must create a terraform access token
# User must also configure the AWS Credentials in Terraform
# S3 Buckets are currently publicly accessible - it can be made private later
# REPORT SQL Queries are incorrect - no group by and date range is out of bounds (start > end)