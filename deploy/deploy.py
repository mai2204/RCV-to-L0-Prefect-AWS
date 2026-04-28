from prefect import flow

def deploy():
    my_flow = flow.from_source(
        source="https://github.com/your-repo/project.git",
        entrypoint="dags/L1/ecom/ecom_flow.py:ecom_flow"
    )

    my_flow.deploy(
        name="ecom-prod-deploy",
        work_pool_name="serverless-pool",
        job_variables={
            "env": {
                "EXTRA_PIP_PACKAGES": "boto3 pandas"
            }
        }
    )

if __name__ == "__main__":
    deploy()