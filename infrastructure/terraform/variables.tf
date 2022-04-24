# variable "access_key" {
#   type        = string
#   description = "Please enter your access key"
#   sensitive   = true
# }

# variable "secret_key" {
#   type        = string
#   description = "Please enter your secret key"
#   sensitive   = true
# }

variable "region_name" {
  type        = string
  description = "Please enter your region name for deploy"
  default     = "eu-central-1"
}

variable "availability_zones" {
  type    = list(string)
  default = ["eu-central-1a", "eu-central-1b"]
}

variable "cluster_name" {
  type        = string
  default     = "whatweather-cluster"
  description = "Please enter your EKS name"
}

variable "vpc_cidr" {
  type        = string
  description = "Please enter CIDR for your VPC"
  default     = "10.0.0.0/16"
}

variable "private_subnets" {
  type        = list(string)
  description = "Please enter PRIVATE subnets"
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnets" {
  type        = list(string)
  description = "Please enter PUBLIC subnets"
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "common_tags" {
  type        = map(any)
  description = "Please enter your common tags for services"
  default = {
    Owners  = "Valentin Kozlov"
    Builder = "by Terraform"
  }
}

variable "db_engine" {
  description = "Please enter engine for your DB"
  type        = string
  default     = "mariadb"
}

variable "db_engine_version" {
  description = "Please enter engine version for your DB"
  type        = string
  default     = "10.6.7"
}

variable "db_instance_class" {
  description = "Please enter instance type for your DB"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Please enter name your DB"
  type        = string
}

variable "db_username" {
  description = "Please enter your username for DB"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Please enter your password for DB user"
  type        = string
  sensitive   = true
}

variable "db_port" {
  description = "Please enter port for DB"
  type        = string
  default     = "3306"
}