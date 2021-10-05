import argparse

from libs.gbigquery import (
    create_dataset,
    load_table_from_uri,
)


def main():
    parser = argparse.ArgumentParser(description='Google Cloud BigQuery tools')
    subparsers = parser.add_subparsers(title='Command', metavar='', dest='command')

    sp_create_dataset = subparsers.add_parser(
        'create_dataset',
        help=('Create dataset')
    )
    sp_create_dataset.add_argument(
        'dataset_name'
    )

    sp_load_table_from_uri = subparsers.add_parser(
        'load_table_from_uri',
        help=("Load table from Google Cloud Storage URI")
    )
    sp_load_table_from_uri.add_argument(
        'uri',
        help='object uri'
    )
    sp_load_table_from_uri.add_argument(
        'dataset',
        help=('Dataset name')
    )
    sp_load_table_from_uri.add_argument(
        'table',
        help=('Table name')
    )

    args = parser.parse_args()

    if args.command == 'create_dataset':
        create_dataset(
            args.dataset_name
        )
    elif args.command == 'load_table_from_uri':
        load_table_from_uri(
            args.uri,
            args.dataset,
            args.table
        )
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
