variable "yfinance_fx_lambda_df_to_parquet_name" {
    type = string
    default = "yfinance_fx_df_to_parquet"
}

variable "yfinance_fx_transformation_name" {
    type = string
    default = "yfinance_fx_transformation"
}


variable "db_credentials_val_data" {
  type = string
  sensitive = true
  nullable=false
}