resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

    tags = merge(var.common_tags,
  { Name = "igw-weather" })
}