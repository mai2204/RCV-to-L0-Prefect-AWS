# Common/module/ingest.py

import pandas as pd
import boto3
import sys

def ingest_table_def_into_dynamodb_from_excel(path, dynamodb_table_name='l0-table-info'):
    df = pd.read_excel(path)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)

    with table.batch_writer() as batch:
        for _, row in df.iterrows():
            item = {
                "system_name": row["system_name"],
                "table_column": f"{row['table_name']}#{row['column_name']}",
                "table_name": row["table_name"],
                "column_name": row["column_name"],
                "data_type": row["data_type"],
                "digit": int(row["digit"]),
                "is_personal_information": bool(row["is_personal_information"]),
                "standardization_def": row.get("standardization_def", "")
            }
            batch.put_item(Item=item)

    print("✅ Loaded metadata into DynamoDB")

# run_ingest.py
if __name__ == "__main__":
    excel_path = sys.argv[1]
    ingest_table_def_into_dynamodb_from_excel(excel_path)