
locals {
  resource_name_prefix = "${var.project_name}-${var.environment}"

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Create the private S3 bucket for the environment.
resource "aws_s3_bucket" "app_storage" {
  # Documented security exceptions for the cost-conscious MVP.
  # Reassess these controls before production use.
  #checkov:skip=CKV_AWS_18:Access logging deferred until a dedicated logging destination is required.
  #checkov:skip=CKV_AWS_144:Cross-region replication deferred until disaster recovery requirements justify the additional cost.
  #checkov:skip=CKV2_AWS_62:Event notifications deferred because the MVP has no event-driven S3 workflow.
  #checkov:skip=CKV_AWS_145:SSE-S3 AES256 is used for this MVP; KMS encryption is deferred pending security and compliance requirements.

  bucket_prefix = "${local.resource_name_prefix}-storage-"

  force_destroy = false

  tags = merge(local.common_tags, {
    Name = "${local.resource_name_prefix}-storage"
  })
}

# Block public access at the bucket level.
resource "aws_s3_bucket_public_access_block" "app_storage" {
  bucket = aws_s3_bucket.app_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable SSE-S3 (AES256) encryption at rest.
resource "aws_s3_bucket_server_side_encryption_configuration" "app_storage" {
  bucket = aws_s3_bucket.app_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }

    bucket_key_enabled = false
  }
}

# Keep object versions so accidental overwrites can be recovered.
resource "aws_s3_bucket_versioning" "app_storage" {
  bucket = aws_s3_bucket.app_storage.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Manage old object versions and incomplete uploads.
resource "aws_s3_bucket_lifecycle_configuration" "app_storage" {
  bucket = aws_s3_bucket.app_storage.id

  # Expire noncurrent object versions after 30 days.
  rule {
    id     = "expire-noncurrent-versions"
    status = "Enabled"

    filter {}

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }

  # Abort incomplete multipart uploads after 7 days.
  rule {
    id     = "abort-incomplete-multipart-uploads"
    status = "Enabled"

    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  depends_on = [
    aws_s3_bucket_versioning.app_storage
  ]
}
