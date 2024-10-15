#tfsec:ignore:aws-s3-enable-bucket-logging
#tfsec:ignore:aws-s3-enable-versioning
#tfsec:ignore:aws-s3-encryption-customer-key
#tfsec:ignore:aws-s3-enable-bucket-encryption
resource "aws_s3_bucket" "s3_ae_exam_bucket" {
  bucket = "ae-exam-bucket-${var.env}"
}

#tfsec:ignore:aws-s3-block-public-acls
#tfsec:ignore:aws-s3-no-public-buckets
#tfsec:ignore:aws-s3-block-public-policy
#tfsec:ignore:aws-s3-ignore-public-acls
resource "aws_s3_bucket_public_access_block" "s3_ae_exam_bucket" {
  bucket = aws_s3_bucket.s3_ae_exam_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "policy" {
  bucket = aws_s3_bucket.s3_ae_exam_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.s3_ae_exam_bucket.arn}/*"
      }
    ]
  })

  depends_on = [
    aws_s3_bucket.s3_ae_exam_bucket,
    aws_s3_bucket_public_access_block.s3_ae_exam_bucket
  ]
}