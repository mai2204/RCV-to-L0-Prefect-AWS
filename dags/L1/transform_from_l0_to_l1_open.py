# transform_from_l0_to_l1_open.py

import boto3
import pandas as pd
from utils.convert_functions import convert_null, convert_datetime

FUNCTION_MAP = {
    "convert_null()": convert_null,
    "convert_datetime()": convert_datetime
}

def get_mapping(system_name, table_name, dynamodb_table_name='l0-table-info'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)

    response = table.query(
        KeyConditionExpression=
            boto3.dynamodb.conditions.Key('system_name').eq(system_name)
    )

    items = response['Items']

    # filter table_name
    return [i for i in items if i["table_name"] == table_name]


def transform_from_l0_to_l1(df: pd.DataFrame, system_name, table_name):
    mapping = get_mapping(system_name, table_name)

    for col_def in mapping:
        col = col_def["column_name"]
        is_pii = col_def["is_personal_information"]
        func_name = col_def["standardization_def"]

        # Apply PII masking
        if is_pii:
            df[col] = convert_null(df[col])

        # Apply transformation function
        if func_name and func_name in FUNCTION_MAP:
            df[col] = FUNCTION_MAP[func_name](df[col])

    return df