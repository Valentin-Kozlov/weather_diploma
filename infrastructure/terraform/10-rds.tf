resource "aws_security_group" "rds" {
  name        = "SG_for_RDS"
  description = "Allow MySQL inbound traffic"
  vpc_id      = aws_vpc.vpc.id
  ingress {
    description = "SG for RDS"
    from_port   = "3306"
    to_port     = "3306"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = merge(var.common_tags, { Name = "RDS" })
}

resource "aws_db_subnet_group" "default" {
  name       = "main"
  subnet_ids = [aws_subnet.private-subnet-A.id, aws_subnet.private-subnet-B.id]
}

resource "aws_db_instance" "db_prod" {
  identifier_prefix       = "db-prod-"
  engine                  = var.db_engine
  engine_version          = var.db_engine_version
  instance_class          = var.db_instance_class
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  port                    = var.db_port
  publicly_accessible     = false
  allocated_storage       = 20
  max_allocated_storage   = 0
  storage_type            = "gp2"
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  skip_final_snapshot     = true
  storage_encrypted       = true
  backup_retention_period = 7
  tags                    = merge(var.common_tags, { Name = "db-prod" })
}

resource "aws_db_instance" "db_dev" {
  identifier_prefix       = "db-dev-"
  engine                  = var.db_engine
  engine_version          = var.db_engine_version
  instance_class          = var.db_instance_class
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  port                    = var.db_port
  publicly_accessible     = false
  allocated_storage       = 20
  max_allocated_storage   = 0
  storage_type            = "gp2"
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  skip_final_snapshot     = true
  storage_encrypted       = true
  backup_retention_period = 7
  tags                    = merge(var.common_tags, { Name = "db-dev" })
}