import sys
import json

from google.cloud import bigquery
from google.oauth2 import service_account


CRED_PATH = "google_cred.json"
PROJECT_ID = "sol-telemetry-prod"
LOCATION = "asia-east2"

CREDENTIALS = service_account.Credentials.from_service_account_file(CRED_PATH)
CLIENT = bigquery.Client(project=PROJECT_ID, credentials=CREDENTIALS)


def get_data(query):
    """
    :param query:
    :param event:
    :return:
    """
    try:
        # Make an API request
        query_job = CLIENT.query(query)
        return query_job

    except Exception as error:
        tb = sys.exc_info()[2]
        print(f"Data read error. Details: {tb.tb_lineno} {error}")
        return []


def save_data(json_data: json, dataset_id, table_id):
    try:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = LOCATION
        table_ref = dataset.table(table_id)
        table = CLIENT.get_table(table_ref)

        errors = CLIENT.insert_rows(table, json_data)
        if not errors:
            return "success"
        else:
            error = errors[0]["errors"]
            message = error[0]["message"]
            return message

    except Exception as error:
        return f"Data saving error. Details: {error}"
