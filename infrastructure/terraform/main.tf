terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.8.0"
    }
  }
  required_version = ">= 1.1.7"
}

provider "aws" {
  region     = var.region_name
  access_key = var.access_key
  secret_key = var.secret_key
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id  
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

data "aws_availability_zones" "zones" {}


resource "aws_security_group" "worker_group_mngt_one" {
  name_prefix = "worker_group_mngt_one"
  vpc_id = module.vpc.vpc_id
    
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"

    cidr_blocks = [
      "10.0.0.0/8",
    ]
  }
  tags = var.common_tags
}

resource "aws_security_group" "all_worker_mngt" {
  name_prefix = "all_worker_mngt"
  vpc_id = module.vpc.vpc_id
    
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"

    cidr_blocks = [
      "10.0.0.0/8",
      "172.16.0.0/12",
      "192.168.0.0/16",
    ]
  }
  tags = var.common_tags
}


module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "3.14.0"

  name = "vpc-diploma"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_gateway = true

  tags = var.common_tags
}


module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"
  vpc_id = module.vpc.vpc_id

  cluster_name = var.cluster_name
  cluster_version = "1.21"

  subnets = module.vpc.private_subnets
  cluster_endpoint_private_access = true
  
  worker_groups = [{
    
  }]
}