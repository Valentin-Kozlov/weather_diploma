resource "aws_subnet" "private-subnet-A" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.private_subnets[0]
  availability_zone = var.availability_zones[0]

  tags = merge(var.common_tags,
    { Name                              = "private-subnets-${var.availability_zones[0]}",
      "kubernetes.io/role/internal-elb" = "1",
  "kubernetes.io/cluster/${var.cluster_name}" = "owned" })
}

resource "aws_subnet" "private-subnet-B" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.private_subnets[1]
  availability_zone = var.availability_zones[1]

  tags = merge(var.common_tags,
    { Name                              = "private-subnets-${var.availability_zones[1]}",
      "kubernetes.io/role/internal-elb" = "1",
  "kubernetes.io/cluster/${var.cluster_name}" = "owned" })
}

resource "aws_subnet" "public-subnet-A" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.public_subnets[0]
  availability_zone       = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = merge(var.common_tags,
    { Name                     = "public-subnets-${var.availability_zones[0]}",
      "kubernetes.io/role/elb" = "1",
  "kubernetes.io/cluster/${var.cluster_name}" = "owned" })
}

resource "aws_subnet" "public-subnet-B" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.public_subnets[1]
  availability_zone       = var.availability_zones[1]
  map_public_ip_on_launch = true

  tags = merge(var.common_tags,
    { Name                     = "public-subnets-${var.availability_zones[1]}",
      "kubernetes.io/role/elb" = "1",
  "kubernetes.io/cluster/${var.cluster_name}" = "owned" })
}
