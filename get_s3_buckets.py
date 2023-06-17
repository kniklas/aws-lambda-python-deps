"""Example of listing all S3 buckets in an AWS account."""

import boto3


s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)
