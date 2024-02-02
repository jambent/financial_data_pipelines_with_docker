##############################################################################
# FX ingestion lambda                                                                 #
##############################################################################

resource "aws_lambda_function" "yfinance_fx_dataframe_to_parquet" {
  function_name = var.yfinance_fx_lambda_df_to_parquet_name
  role          = aws_iam_role.yfinance_fx_lambda_df_to_parquet_role.arn
  s3_bucket     = aws_s3_bucket.code_bucket.id
  s3_key        = aws_s3_object.yfinance_fx_ingestion_code.key
  handler       = "yfinance_fx_ingestion.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60
  environment {
    variables = {
      "S3_LANDING_ID"          = aws_s3_bucket.landing_bucket.id,
      "S3_LANDING_ARN"         = aws_s3_bucket.landing_bucket.arn
    }
  }
  layers = [
            "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:4",
            aws_lambda_layer_version.yfinance_layer.arn
        ]

}

resource "aws_lambda_permission" "allow_0600_events" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.yfinance_fx_dataframe_to_parquet.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.yfinance_fx_ingestion_lambda_0600_invocation_rule.arn
  source_account = data.aws_caller_identity.current.account_id
}

resource "aws_lambda_permission" "allow_1630_events" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.yfinance_fx_dataframe_to_parquet.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.yfinance_fx_ingestion_lambda_1630_invocation_rule.arn
  source_account = data.aws_caller_identity.current.account_id
}

resource "aws_lambda_permission" "allow_2000_events" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.yfinance_fx_dataframe_to_parquet.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.yfinance_fx_ingestion_lambda_2000_invocation_rule.arn
  source_account = data.aws_caller_identity.current.account_id
}



##############################################################################
# FX transformation lambda                                                                 #
##############################################################################
/*
resource "aws_lambda_function" "yfinance_fx_transformation" {
  function_name = var.yfinance_fx_transformation_name
  role          = aws_iam_role.yfinance_fx_lambda_df_to_parquet_role.arn
  s3_bucket     = aws_s3_bucket.code_bucket.id
  s3_key        = aws_s3_object.yfinance_fx_transformation_code.key
  handler       = "yfinance_fx_transformation.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60
  environment {
    variables = {
      "S3_LANDING_ID"          = aws_s3_bucket.landing_bucket.id,
      "S3_LANDING_ARN"         = aws_s3_bucket.landing_bucket.arn
    }
  }
  layers = [
            "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:4"
        ]

}*/