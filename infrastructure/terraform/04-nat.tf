resource "aws_eip" "nat" {
  vpc = true

  tags = merge(var.common_tags,
  { Name = "nat-weather" })
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public-subnet-A.id

  tags = merge(var.common_tags,
  { Name = "nat-weather" })

  depends_on = [aws_internet_gateway.igw]
}