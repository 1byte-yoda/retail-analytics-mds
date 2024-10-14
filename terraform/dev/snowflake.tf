resource "snowflake_warehouse" "exam_wh" {
  name           = "EXAM_WH_${upper(var.env)}"
  auto_suspend   = 20
  warehouse_size = "small"
}

resource "snowflake_database" "platform_db" {
  name = "PLATFORM_${upper(var.env)}"
}

resource "snowflake_account_role" "transform" {
  name = "TRANSFORM_${upper(var.env)}"
}

resource "snowflake_grant_account_role" "accountadmin_to_transform" {
  role_name        = snowflake_account_role.transform.name
  parent_role_name = "ACCOUNTADMIN"
}


resource "snowflake_grant_privileges_to_account_role" "transform_operate_wh" {
  privileges        = ["OPERATE"]
  account_role_name = snowflake_account_role.transform.name
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.exam_wh.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "transform_all_wh" {
  account_role_name = snowflake_account_role.transform.name
  all_privileges    = true
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.exam_wh.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "transform_all_db" {
  account_role_name = snowflake_account_role.transform.name
  all_privileges    = true
  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.platform_db.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "transform_all_schemas" {
  account_role_name = snowflake_account_role.transform.name
  all_privileges    = true
  on_schema {
    all_schemas_in_database = snowflake_database.platform_db.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "transform_future_schemas" {
  account_role_name = snowflake_account_role.transform.name
  all_privileges    = true
  on_schema {
    future_schemas_in_database = snowflake_database.platform_db.name
  }
}


# RAW Schema
resource "snowflake_schema" "platform_db_schema_raw" {
  database = snowflake_database.platform_db.name
  name     = "RAW"
}

resource "snowflake_grant_privileges_to_account_role" "transform_all_tables_in_raw" {
  account_role_name = snowflake_account_role.transform.name
  all_privileges    = true
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_schema          = snowflake_schema.platform_db_schema_raw.fully_qualified_name
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "transform_future_tables_in_raw" {
  account_role_name = snowflake_account_role.transform.name
  all_privileges    = true
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_schema          = snowflake_schema.platform_db_schema_raw.fully_qualified_name
    }
  }
}

#
# resource "snowflake_table_grant" "all_tables_raw" {
#   database_name = snowflake_database.platform_db.name
#   schema_name   = snowflake_schema.platform_dev_raw.name
#   privilege     = "ALL"
#   roles         = [snowflake_role.transform.name]
#   on_all        = true
# }
#
# resource "snowflake_table_grant" "all_future_tables_raw" {
#   database_name = snowflake_database.platform_db.name
#   schema_name   = snowflake_schema.platform_dev_raw.name
#   privilege     = "ALL"
#   roles         = [snowflake_role.transform.name]
#   on_future     = true
# }
#
# # DIM Schema
# resource "snowflake_schema" "platform_dev_dim" {
#   database = snowflake_database.platform_db.name
#   name     = "DIM"
# }
#
# resource "snowflake_table_grant" "all_tables_dim" {
#   database_name = snowflake_database.platform_db.name
#   schema_name   = snowflake_schema.platform_dev_dim.name
#   privilege     = "ALL"
#   roles         = [snowflake_role.transform.name]
#   on_all        = true
# }
#
# resource "snowflake_table_grant" "all_future_tables_dim" {
#   database_name = snowflake_database.platform_db.name
#   schema_name   = snowflake_schema.platform_dev_dim.name
#   privilege     = "ALL"
#   roles         = [snowflake_role.transform.name]
#   on_future     = true
# }
#
# # MART Schema
# resource "snowflake_schema" "platform_dev_mart" {
#   database = snowflake_database.platform_db.name
#   name     = "MART"
# }
#
# resource "snowflake_table_grant" "all_tables_mart" {
#   database_name = snowflake_database.platform_db.name
#   schema_name   = snowflake_schema.platform_dev_mart.name
#   privilege     = "ALL"
#   roles         = [snowflake_role.transform.name]
#   on_all        = true
# }
#
# resource "snowflake_table_grant" "all_future_tables_mart" {
#   database_name = snowflake_database.platform_db.name
#   schema_name   = snowflake_schema.platform_dev_mart.name
#   privilege     = "ALL"
#   roles         = [snowflake_role.transform.name]
#   on_future     = true
# }
#
# resource "snowflake_schema_grant" "all_privileges_schemas" {
#   database_name = snowflake_database.platform_db.name
#   privilege     = "ALL"
#   roles         = [snowflake_role.transform.name]
#   on_all        = true
# }
#
# resource "snowflake_schema_grant" "all_future_schemas_privileges" {
#   database_name  = snowflake_database.platform_db.name
#   privilege      = "ALL"
#   roles          = [snowflake_role.transform.name]
#   on_future      = true
# }