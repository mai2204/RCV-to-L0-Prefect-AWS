from prefect import flow, task
from transform_from_l0_to_l1_open import transform_from_l0_to_l1

@task
def load_data():
    # load L0 data (S3, etc.)
    return df

@task
def transform(df):
    return transform_from_l0_to_l1(df, "ecom", "order_reviews")

@flow
def l1_pipeline():
    df = load_data()
    df_transformed = transform(df)
    return df_transformed