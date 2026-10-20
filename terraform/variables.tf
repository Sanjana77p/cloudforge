
variable "aws_region" {
  description = "AWS region where CloudForge resources will be deployed"
  type        = string
  default     = "us-east-1"

  validation {
    condition = contains([
      "us-east-1",
      "us-east-2",
      "us-west-1",
      "us-west-2",
      "ap-south-1",
      "ap-southeast-1",
      "ap-southeast-2",
      "eu-west-1",
      "eu-central-1"
    ], var.aws_region)

    error_message = "The AWS region must be one of the approved CloudForge regions."
  }
}

variable "project_name" {
  description = "Name used to identify CloudForge resources"
  type        = string
  default     = "cloudforge"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,29}$", var.project_name))
    error_message = "Project name must be 3-30 characters, start with a lowercase letter, and contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
