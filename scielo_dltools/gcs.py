import argparse

from libs.gstorage import (
    download_file,
    get_metadata,
    list_content,
    rename_file,
    upload_file,
)


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
