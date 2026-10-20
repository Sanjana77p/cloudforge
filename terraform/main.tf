
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}


module "app_environment" {
  source = "./modules/app_environment"

  project_name       = var.project_name
  environment        = var.environment
  instance_size      = "small"
  monthly_budget_usd = 5
}
