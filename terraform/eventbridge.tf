##############################################################################
# FX rules                                                              
##############################################################################


resource "aws_cloudwatch_event_rule" "yfinance_fx_ingestion_lambda_0600_invocation_rule" {
  name                = "yfinance-fx-ingestion-lambda-0600-invocation-event-rule"
  description         = "triggers yfinance fx ingestion lambda according to specified schedule"
  schedule_expression = "cron(20 06 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "yfinance_fx_ingestion_lambda_0600_target" {
  arn  = aws_lambda_function.yfinance_fx_dataframe_to_parquet.arn
  rule = aws_cloudwatch_event_rule.yfinance_fx_ingestion_lambda_0600_invocation_rule.name
}


resource "aws_cloudwatch_event_rule" "yfinance_fx_ingestion_lambda_1630_invocation_rule" {
  name                = "yfinance-fx-ingestion-lambda-1630-invocation-event-rule"
  description         = "triggers yfinance fx ingestion lambda according to specified schedule"
  schedule_expression = "cron(50 16 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "yfinance_fx_ingestion_lambda_1630_target" {
  arn  = aws_lambda_function.yfinance_fx_dataframe_to_parquet.arn
  rule = aws_cloudwatch_event_rule.yfinance_fx_ingestion_lambda_1630_invocation_rule.name
}


resource "aws_cloudwatch_event_rule" "yfinance_fx_ingestion_lambda_2000_invocation_rule" {
  name                = "yfinance-fx-ingestion-lambda-2000-invocation-event-rule"
  description         = "triggers yfinance fx ingestion lambda according to specified schedule"
  schedule_expression = "cron(20 20 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "yfinance_fx_ingestion_lambda_2000_target" {
  arn  = aws_lambda_function.yfinance_fx_dataframe_to_parquet.arn
  rule = aws_cloudwatch_event_rule.yfinance_fx_ingestion_lambda_2000_invocation_rule.name
}

##############################################################################
# Equity Index rules                                                              
##############################################################################


resource "aws_cloudwatch_event_rule" "yfinance_equity_index_ingestion_lambda_1615_invocation_rule" {
  name                = "yfinance-eq-index-ingestion-lambda-1615-invocation-event-rule"
  description         = "triggers yfinance equity index ingestion lambda according to specified schedule"
  schedule_expression = "cron(35 16 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "yfinance_equity_index_ingestion_lambda_1615_target" {
  arn  = aws_lambda_function.yfinance_equity_index_dataframe_to_parquet.arn
  rule = aws_cloudwatch_event_rule.yfinance_equity_index_ingestion_lambda_1615_invocation_rule.name
}
