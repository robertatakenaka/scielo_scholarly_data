import argparse

from google.cloud import bigquery
from google.api_core.exceptions import Conflict, Forbidden


def _connect():
    return bigquery.Client()


