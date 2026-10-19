
output "aws_region" {
  description = "AWS region configured for CloudForge"
  value       = var.aws_region
}

output "project_name" {
  description = "CloudForge project name"
  value       = var.project_name
}

output "environment" {
  description = "CloudForge deployment environment"
  value       = var.environment
}
