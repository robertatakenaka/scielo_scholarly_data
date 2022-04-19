import os
import argparse
import json
import csv
from html import unescape


def read_file(input_file_path, encoding="utf-8"):
    with open(input_file_path, "r", encoding=encoding) as fp:
        for row in fp.readlines():
            yield row.strip()


def jsonl_to_csv(jsonl_file_path, json_file_encoding, csv_file_path, fieldnames):
    dirname = os.path.dirname(csv_file_path)
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)

    with open(csv_file_path, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in read_file(jsonl_file_path, json_file_encoding):
            try:
                data = json.loads(row.strip())
            except Exception as e:
                print(e)
            try:
                for k in data.keys():
                    data[k] = unescape(data[k])
                writer.writerow(data)
            except Exception as e:
                print(e)


def main():
    parser = argparse.ArgumentParser(description="JSON to CSV tool")
    subparsers = parser.add_subparsers(title="Commands", metavar="", dest="command")

    op_parser = subparsers.add_parser(
        'j2c',
        help=(
            "Create a CSV file from a given JSON"
        )
    )
    op_parser.add_argument(
        'jsonl_file_path',
        help='json file path. E.g.: /path/source.jsonl'
    )
    op_parser.add_argument(
        'jsonl_file_encoding',
        help='jsonl file encoding. E.g.: iso-8859-1'
    )
    op_parser.add_argument(
        'output_csv_file_path',
        help='csv file path. E.g.: /path/destination.csv'
    )
    op_parser.add_argument(
        'fieldnames',
        help='Field names of CSV file. E.g.: "pid,aff_id,aff_orgdiv3,aff_orgdiv2,aff_orgdiv1,aff_country,aff_city,aff_state,aff_orgname,aff_status"'
    )

    args = parser.parse_args()
    if args.command == "j2c":
        jsonl_to_csv(
            args.jsonl_file_path,
            args.jsonl_file_encoding,
            args.output_csv_file_path,
            args.fieldnames.split(","),
        )
    else:
        parser.print_help()
    print("""
        # python scielo_dltools/utils/jsonl2csv.py j2c a.jsonl iso-8859-1 a.csv "pid,aff_id,aff_orgdiv3,aff_orgdiv2,aff_orgdiv1,aff_country,aff_city,aff_state,aff_orgname,aff_status"
    """)


if __name__ == '__main__':
    main()
