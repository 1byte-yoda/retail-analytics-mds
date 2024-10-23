terraform {
  required_version = "~> 1.8"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "0.97.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
  cloud {
    organization = "1byte-yoda"
    workspaces {
      name = "data-junkie-corp-dev"
    }
  }

}
provider "aws" {
  region = "ap-southeast-2"
}
provider "snowflake" {
  account  = var.snowflake_account
  user     = var.snowflake_username
  password = var.snowflake_password
  role     = var.snowflake_role
}