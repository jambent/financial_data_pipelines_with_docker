resource "aws_secretsmanager_secret" "db_creds_val_data" {
  name = "db_credentials_val_data"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db_creds_val_data" {
  secret_id     = aws_secretsmanager_secret.db_creds_val_data.id
  secret_string = var.db_credentials_val_data
}