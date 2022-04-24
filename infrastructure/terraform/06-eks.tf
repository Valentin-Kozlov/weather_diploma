resource "aws_iam_role" "weather-cluster" {
  name = var.cluster_name

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "weather-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.weather-cluster.name
}

resource "aws_iam_role_policy_attachment" "eks-vpc-policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.weather-cluster.name
}

resource "aws_eks_cluster" "weather-cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.weather-cluster.arn
  version  = "1.21"


  vpc_config {
    endpoint_private_access = false
    endpoint_public_access  = true
    subnet_ids = [
      aws_subnet.private-subnet-A.id,
      aws_subnet.private-subnet-B.id,
      aws_subnet.public-subnet-A.id,
      aws_subnet.public-subnet-B.id
    ]
  }

  depends_on = [aws_iam_role_policy_attachment.weather-AmazonEKSClusterPolicy]
  tags = merge(var.common_tags,
  { Name = "eks-diploma" })
}