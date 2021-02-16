import boto3

def upload_file(filename, bucket):
    
    object_name = filename
    client = boto3.client("s3")
    response = client.upload_file(filename, bucket, object_name)

    return response