##############################################################################
# Log groups
##############################################################################
resource "aws_cloudwatch_log_group" "yfinance_fx_dataframe_to_parquet_logs" {
  name = "/aws/lambda/${aws_lambda_function.yfinance_fx_dataframe_to_parquet.function_name}"
  depends_on = [aws_lambda_function.yfinance_fx_dataframe_to_parquet]
}