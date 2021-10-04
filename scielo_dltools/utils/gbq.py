import argparse

from google.cloud import bigquery
from google.api_core.exceptions import Conflict, Forbidden


def _connect():
    return bigquery.Client()


def _generate_dataset_id(project_name, dataset_name):
    return '{}.{}'.format(project_name, dataset_name)


def _generate_table_id(project_name, dataset_name, table_id):
    return '{}.{}.{}'.format(project_name, dataset_name, table_id)


