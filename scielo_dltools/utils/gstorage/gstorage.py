import argparse

from datetime import datetime
from google.cloud import storage
from google.api_core.exceptions import NotFound


def _connect(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)


def list_content(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for b in bucket.list_blobs():
        print(b.name)


def download_file(bucket_name, source_file_name, destination_file_name):
    bucket = _connect(bucket_name)
    blob = bucket.blob(source_file_name)

    try:
        blob.download_to_filename(destination_file_name)
    except NotFound:
        print('No such file or directory ({}) or bucket name ({})'.format(source_file_name, bucket_name))
    except IsADirectoryError:
        print('Destination file name {} could not be a directory'.format(destination_file_name))
    else:
        print('Downloaded storage object {} from bucket {} to local file {}.'.format(source_file_name, bucket_name, destination_file_name))


def upload_file(bucket_name, source_file_name, destination_file_name):
    bucket = _connect(bucket_name)
    blob = bucket.blob(destination_file_name)
    blob.metadata = {'upload_datetime': datetime.utcnow()}

    try:
        blob.upload_from_filename(source_file_name)
    except FileNotFoundError:
        print('No such file or directory: {}'.format(source_file_name))
    else:
        print('File {} uploaded to {}.'.format(source_file_name, destination_file_name))


def rename_file(bucket_name, source_file_name, destination_file_name):
    bucket = _connect(bucket_name)

    try:
        blob = bucket.get_blob(source_file_name)
        bucket.rename_blob(blob, destination_file_name)
    except FileNotFoundError:
        print('No such file or directory: {}'.format(source_file_name))
    else:
        'File {} renamed to {}.'.format(source_file_name, destination_file_name)

