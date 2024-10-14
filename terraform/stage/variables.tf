variable "env" {
  description = "The Environment Variable in which the Infrastructure will get created"
  default = "stage"
}

variable "snowflake_account" {
  description = "The Assigned Snowflake Account ID"
}

variable "snowflake_username" {
  description = "The username for logging in"
}

variable "snowflake_password" {
  description = "The password for logging in"
}

variable "snowflake_role" {
  description = "The role to used for infrastructure manipulation"
}