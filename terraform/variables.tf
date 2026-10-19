
variable "aws_region" {
  description = "AWS region where CloudForge resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name used to identify CloudForge resources"
  type        = string
  default     = "cloudforge"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
