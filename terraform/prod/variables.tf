variable "env" {
  description = "The Environment Variable in which the Infrastructure will get created"
  default     = "prod"
  type = string
}

variable "snowflake_account" {
  description = "The Assigned Snowflake Account ID"
  type = string
}

variable "snowflake_username" {
  description = "The username for logging in"
  type = string
}

variable "snowflake_password" {
  description = "The password for logging in"
  type = string
}

variable "snowflake_role" {
  description = "The role to used for infrastructure manipulation"
  type = string
}