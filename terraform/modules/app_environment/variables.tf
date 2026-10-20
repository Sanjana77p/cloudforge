
variable "project_name" {
  description = "Name of the CloudForge project"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,29}$", var.project_name))
    error_message = "Project name must be 3-30 characters, start with a lowercase letter, and contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Target environment"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_size" {
  description = "Requested application instance size"
  type        = string
  default     = "small"

  validation {
    condition     = contains(["small", "medium"], var.instance_size)
    error_message = "Instance size must be small or medium."
  }
}

variable "monthly_budget_usd" {
  description = "Maximum requested monthly budget in USD"
  type        = number
  default     = 5

  validation {
    condition     = var.monthly_budget_usd > 0 && var.monthly_budget_usd <= 5
    error_message = "Monthly budget must be greater than zero and no more than 5 USD."
  }
}
