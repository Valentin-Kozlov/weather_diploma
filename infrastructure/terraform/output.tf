output "tls-certificate-eks" {
  description = "tls certificate eks"
  value       = data.tls_certificate.eks
}

output "dns_name_db_prod" {
  description = "dns db prod"
  value       = aws_db_instance.db_prod.address
}

output "dns_name_db_dev" {
  description = "dns db dev"
  value       = aws_db_instance.db_dev.address
}