resource "aws_db_instance" "default" {
  allocated_storage = 5
  engine = "postgres"
  instance_class = "db.t3.micro"
  username = "val_user"
  password = aws_secretsmanager_secret_version.db_creds_val_data.secret_string
  skip_final_snapshot = true // required to destroy

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name = aws_db_subnet_group.val_data_db_subnet_group.name
}


resource "aws_db_subnet_group" "val_data_db_subnet_group" {
  name = "val-data-db-subnet-group"
  subnet_ids = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]

  tags = {
    Name = "Val Data DB Subnet Group"
  }
}