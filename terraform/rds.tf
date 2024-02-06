resource "aws_db_instance" "default" {
  allocated_storage = 5
  db_name = "val_data"
  engine = "postgres"
  instance_class = "db.t3.micro"
  parameter_group_name = aws_db_parameter_group.switch_off_force_ssl.name
  username = local.username
  password = local.password
  skip_final_snapshot = true // required to destroy

  publicly_accessible = true
}


resource "aws_db_parameter_group" "switch_off_force_ssl" {
  name   = "db-ssl-params"
  family = "postgres15"

  parameter {
    apply_method = "immediate"
    name         = "rds.force_ssl"
    value        = 0
  }
}

