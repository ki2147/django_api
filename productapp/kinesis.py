import boto3
from decouple import config


# Get the AWS credentials from environment variables
aws_access_key_id = config('AWS_ACCESS_KEY_ID')
aws_secret_access_key = config('AWS_SECRET_ACCESS_KEY')
aws_region_name = config('AWS_REGION')  # Replace with your desired region


# Create a Kinesis client using the specified credentials
def get_kinesis_client():
    return boto3.client(
        'kinesis',
        region_name=aws_region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
