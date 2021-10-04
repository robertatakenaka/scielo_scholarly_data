import argparse

from google.cloud import bigquery
from google.api_core.exceptions import Conflict, Forbidden


def _connect():
    return bigquery.Client()


def _generate_dataset_id(project_name, dataset_name):
    return '{}.{}'.format(project_name, dataset_name)


def _generate_table_id(project_name, dataset_name, table_id):
    return '{}.{}.{}'.format(project_name, dataset_name, table_id)


def create_dataset(dataset_name):
    bq_client = _connect()
    dataset_id = _generate_dataset_id(bq_client.project, dataset_name)

    try:
        ds = bq_client.create_dataset(dataset_id)
    except Forbidden:
        print('Access denied')
    except Conflict:
        print('Dataset {} already exists'.format(dataset_id))
    else:
        print('Dataset {} created with success'.format(dataset_id))
        return ds
