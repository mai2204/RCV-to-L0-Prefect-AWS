from prefect import flow
from prefect_aws.s3 import S3Bucket
from prefect_aws import AwsCredentials

def deploy():
    s3_bucket_block = S3Bucket.load("dev-code-flow")

    my_flow = flow.from_source(
        source=s3_bucket_block,
        entrypoint="dags/L1/ecom/ecom_flow.py:ecom_flow"
    )

    my_flow.deploy(
        name="ecom-dev-deploy",
        work_pool_name="Serverless",
        job_variables={
            "env": {
                "EXTRA_PIP_PACKAGES": "boto3 pandas prefect-aws"
            }
        }
    )

if __name__ == "__main__":
    deploy()