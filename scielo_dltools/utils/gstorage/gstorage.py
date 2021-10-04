import argparse

from datetime import datetime
from google.cloud import storage
from google.api_core.exceptions import NotFound


def _connect(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)
