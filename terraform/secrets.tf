locals{
    port = var.db_credentials.db_credentials.port
    database = var.db_credentials.db_credentials.database
    username = var.db_credentials.db_credentials.username
    password = var.db_credentials.db_credentials.password
}

variable "db_credentials"{}


resource "aws_secretsmanager_secret" "db_creds_val_data" {
  name = "db_credentials_val_data"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db_creds_val_data" {
  secret_id     = aws_secretsmanager_secret.db_creds_val_data.id
  secret_string = "{\"port\":\"${local.port}\", \"database\":\"${local.database}\",\"username\":\"${local.username}\",\"password\":\"${local.password}\"}"
}