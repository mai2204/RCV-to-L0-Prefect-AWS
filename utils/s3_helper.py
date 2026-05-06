import boto3
from prefect_aws import AwsCredentials


def get_s3_client():
    aws_creds = AwsCredentials.load("aws-credentials")
    return aws_creds.get_boto3_session().client("s3")


def list_files(bucket):
    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket   
        )

        contents = response.get("Contents", [])
        return [obj["Key"] for obj in contents]

    except Exception as e:
        print(f"[ERROR] Cannot list files from bucket: {bucket}")
        raise e

def move_file(source_bucket, key, target_bucket, target_key):
    s3_client = get_s3_client()

    try:
        # Copy
        s3_client.copy_object(
            Bucket=target_bucket,
            CopySource={"Bucket": source_bucket, "Key": key},
            Key=target_key
        )

        # Delete original
        s3_client.delete_object(
            Bucket=source_bucket,
            Key=key
        )

        print(f"Moved: {key} → {target_bucket}/{target_key}")

    except Exception as e:
        print(f"[ERROR] Cannot move file: {key}")
        raise e