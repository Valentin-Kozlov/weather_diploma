resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  tags = merge(var.common_tags,
  { Name = "private" })
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  tags = merge(var.common_tags,
  { Name = "public" })
}



resource "aws_route" "private" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
  depends_on             = [aws_route_table.private]
}

resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
  depends_on             = [aws_route_table.public]
}


resource "aws_route_table_association" "private-A" {
  subnet_id      = aws_subnet.private-subnet-A.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private-B" {
  subnet_id      = aws_subnet.private-subnet-B.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "public-A" {
  subnet_id      = aws_subnet.public-subnet-A.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public-B" {
  subnet_id      = aws_subnet.public-subnet-B.id
  route_table_id = aws_route_table.public.id
}