
# Verify that the default CloudForge inputs are accepted.
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
