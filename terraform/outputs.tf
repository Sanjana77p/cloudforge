
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


output "module_resource_name_prefix" {
  description = "Resource naming prefix from the application module"
  value       = module.app_environment.resource_name_prefix
}

output "module_instance_size" {
  description = "Requested instance size from the application module"
  value       = module.app_environment.instance_size
}

output "module_monthly_budget_usd" {
  description = "Requested monthly budget from the application module"
  value       = module.app_environment.monthly_budget_usd
}

output "s3_bucket_name" {
  description = "Name of the application storage bucket"
  value       = module.app_environment.s3_bucket_name
}

output "s3_bucket_arn" {
  description = "ARN of the application storage bucket"
  value       = module.app_environment.s3_bucket_arn
}