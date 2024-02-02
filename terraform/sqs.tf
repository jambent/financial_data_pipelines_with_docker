data "aws_iam_policy_document" "FX_queue" {
  statement {
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions   = ["sqs:SendMessage"]
    resources = ["arn:aws:sqs:*:*:s3-FX-file-created-notification-queue"]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_s3_bucket.landing_bucket.arn]
    }
  }
}

resource "aws_sqs_queue" "FX_queue" {
  name   = "s3-FX-file-created-notification-queue"
  policy = data.aws_iam_policy_document.FX_queue.json
}