resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = merge(var.common_tags,
  { Name = "vpc-diploma" })
}