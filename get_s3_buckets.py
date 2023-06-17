"""Example of listing all S3 buckets in an AWS account."""

# pylint: disable=unused-import
import requests
import boto3


# pylint: disable=unused-argument
def lambda_handler(event, context):
    """Lambda handler."""

    s3_resource = boto3.resource('s3')
    for bucket in s3_resource.buckets.all():
        print(bucket.name)
