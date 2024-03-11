data "aws_caller_identity" "current" {}

data "archive_file" "df_to_parquet_lambda" {
  type        = "zip"
  source_dir = "${path.module}/../src/yfinance_fx_ingestion"
  output_path = "${path.module}/../lambda_code_zip_files/yfinance_fx_ingestion_function.zip"
}

data "archive_file" "equity_index_df_to_parquet_lambda" {
  type        = "zip"
  source_dir = "${path.module}/../src/yfinance_equity_index_ingestion"
  output_path = "${path.module}/../lambda_code_zip_files/yfinance_equity_index_ingestion_function.zip"
}