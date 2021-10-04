import argparse

from datetime import datetime
from google.cloud import storage
from google.api_core.exceptions import NotFound


def _connect(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)


def list_content(bucket_name):
    bucket = _connect(bucket_name)

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


def get_metadata(bucket_name, source_file_name):
    bucket = _connect(bucket_name)
    try:
        blob = bucket.get_blob(source_file_name)
    except FileNotFoundError:
        print('No such file or directory: {}'.format(source_file_name))
    else:
        if blob and blob.metadata:
            print(blob.metadata)


def main():
    parser = argparse.ArgumentParser(description='Google Cloud Storage tools')
    subparsers = parser.add_subparsers(title='Command', metavar='', dest='command')

    sp_download = subparsers.add_parser(
        'download',
        help=("Download a file")
    )
    sp_download.add_argument(
        'bucket',
        help='Bucket name'
    )
    sp_download.add_argument(
        'source',
        help='Source file name'
    )
    sp_download.add_argument(
        'destination',
        help='Destination file name'
    )

    sp_upload = subparsers.add_parser(
        'upload',
        help=('Upload a file')
    )
    sp_upload.add_argument(
        'bucket',
        help='Bucket name'
    )
    sp_upload.add_argument(
        'source',
        help='Source file name'
    )
    sp_upload.add_argument(
        'destination',
        help='Destination file name'
    )

    sp_list = subparsers.add_parser(
        'list',
        help=('List bucket content')
    )
    sp_list.add_argument(
        'bucket',
        help=('Bucket name')
    )

    sp_rename = subparsers.add_parser(
        'rename',
        help=('Rename file')
    )
    sp_rename.add_argument(
        'bucket',
        help=('Bucket name')
    )
    sp_rename.add_argument(
        'source',
        help=('Original name')
    )
    sp_rename.add_argument(
        'destination',
        help=('New name')
    )

    sp_metatada = subparsers.add_parser(
        'metadata',
        help=('Get metadata')
    )
    sp_metatada.add_argument(
        'bucket',
        help=('Bucket name')
    )
    sp_metatada.add_argument(
        'source',
        help=('Source file name')
    )

    args = parser.parse_args()

    if args.command == 'download':
        download_file(
            args.bucket,
            args.source,
            args.destination
        )
    elif args.command == 'upload':
        upload_file(
            args.bucket,
            args.source,
            args.destination
        )
    elif args.command == 'list':
        list_content(args.bucket)
    elif args.command == 'rename':
        rename_file(
            args.bucket,
            args.source,
            args.destination
        )
    elif args.command == 'metadata':
        get_metadata(
            args.bucket,
            args.source
        )
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
