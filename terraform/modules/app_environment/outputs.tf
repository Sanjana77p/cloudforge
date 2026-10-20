
output "resource_name_prefix" {
  description = "Consistent prefix for CloudForge resource names"
  value       = local.resource_name_prefix
}

output "environment" {
  description = "Target deployment environment"
  value       = var.environment
}

output "instance_size" {
  description = "Requested application instance size"
  value       = var.instance_size
}

output "monthly_budget_usd" {
  description = "Requested monthly budget in USD"
  value       = var.monthly_budget_usd
}

output "common_tags" {
  description = "Standard tags for CloudForge resources"
  value       = local.common_tags
}
