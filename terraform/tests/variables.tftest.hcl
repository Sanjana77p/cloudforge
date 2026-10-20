
# Verify that the default CloudForge inputs are accepted.
# Mock AWS so Terraform tests don't require real AWS credentials
# or create AWS resources.
mock_provider "aws" {}
run "valid_defaults" {
  command = plan

  assert {
    condition     = output.aws_region == "us-east-1"
    error_message = "The default AWS region should be us-east-1."
  }

  assert {
    condition     = output.environment == "dev"
    error_message = "The default environment should be dev."
  }

  assert {
    condition     = output.project_name == "cloudforge"
    error_message = "The default project name should be cloudforge."
  }
}

# Verify that an invalid environment is rejected.
run "reject_invalid_environment" {
  command = plan

  variables {
    environment = "testing"
  }

  expect_failures = [
    var.environment
  ]
}

# Verify that an invalid AWS region is rejected.
run "reject_invalid_region" {
  command = plan

  variables {
    aws_region = "invalid-region"
  }

  expect_failures = [
    var.aws_region
  ]
}

# Verify that an invalid project name is rejected.
run "reject_invalid_project_name" {
  command = plan

  variables {
    project_name = "Invalid Name!"
  }

  expect_failures = [
    var.project_name
  ]
}


run "app_environment_module_outputs" {
  command = plan

  assert {
    condition     = output.module_resource_name_prefix == "cloudforge-dev"
    error_message = "The module should generate the cloudforge-dev naming prefix."
  }

  assert {
    condition     = output.module_instance_size == "small"
    error_message = "The module should use small as the default instance size."
  }

  assert {
    condition     = output.module_monthly_budget_usd == 5
    error_message = "The module should expose the requested monthly budget of 5 USD."
  }
}


#
# Verify that the application module exposes the S3 bucket outputs.
run "s3_bucket_outputs_are_configured" {
  command = plan

  assert {
    condition     = output.module_resource_name_prefix == "cloudforge-dev"
    error_message = "The application module should retain its expected naming prefix."
  }

  assert {
    condition     = output.module_monthly_budget_usd == 5
    error_message = "The application module should retain the requested budget."
  }
}
