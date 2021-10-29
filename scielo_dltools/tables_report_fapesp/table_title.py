import argparse
import csv
import scielo_scholarly_data.standardizer as standardizer

from scielo_dltools.libs import gstorage


def read_table(file_path, skema, table):
    with open(file_path) as data:
        csv_reader = csv.DictReader(data, delimiter=',')
        for row in csv_reader:
            for label in skema[2:]:
                if row.get(label) != '':
                    cols = []
                    cols.append(row.get(skema[1]))
                    cols.append(row.get(label))
                    cols.append(skema[0])
                    cols.append(label)
                    # cols.append(date)
                    table.append(cols)


def write_table(file_path, skema, table):
    with open(file_path, 'w') as out:
        writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(skema)
        for rows in table:
            writer.writerow(rows)


def main():
    parser = argparse.ArgumentParser(description='Create a standardized titles file from data in Data Lake.')
    parser.add_argument('-bnd', action='store', dest='bucket_name_download', required=True,
                        help='Data Lake bucket to download.')
    parser.add_argument('-sfd', action='store', nargs='+', dest='source_file_download', required=True,
                        help='Space-separated list of source files to download.')
    parser.add_argument('-dfd', action='store', nargs='+', dest='destination_file_download', required=True,
                        help='Space-separated list of destination files to download.')
    parser.add_argument('-bnu', action='store', dest='bucket_name_upload', required=True,
                        help='Data Lake bucket to upload.')
    parser.add_argument('-sfu', action='store', nargs='+', dest='source_file_upload', required=True,
                        help='Space-separated list of source files to upload.')
    parser.add_argument('-dfu', action='store', nargs='+', dest='destination_file_upload', required=True,
                        help='Space-separated list of destination files to upload.')
    arguments = parser.parse_args()

    BUCKET_NAME_DOWNLOAD = arguments.bucket_name_download
    SOURCE_FILE_DOWNLOAD = arguments.source_file_download
    DESTINATION_FILE_DOWNLOAD = arguments.destination_file_download
    BUCKET_NAME_UPLOAD = arguments.bucket_name_upload
    SOURCE_FILE_UPLOAD = arguments.source_file_upload
    DESTINATION_FILE_UPLOAD = arguments.destination_file_upload

    skemas_in = [
        [
            'DOAJ (Directory of Open Access Journals)',
            'Journal ISSN (print version)',
            'Journal title',
            'Journal title vis',
            'Journal title dep',
            'Alternative title',
            'Alternative title vis',
            'Alternative title dep'
        ],
        [
            'ISSN International Portal',
            'issn_l',
            'key_title',
            'key_title vis',
            'key_title dep',
            'title_proper',
            'title_proper vis',
            'title_proper dep'
        ]
    ]

    skema_table_out = [
        'issn_SciELO',
        'title',
        'source',
        'label',
        # 'date'
    ]

    table = []

    for source in range(len(SOURCE_FILE_DOWNLOAD)):
        gstorage.download_file(
            BUCKET_NAME_DOWNLOAD,
            SOURCE_FILE_DOWNLOAD[source],
            DESTINATION_FILE_DOWNLOAD[source]
        )
        read_table(DESTINATION_FILE_DOWNLOAD[source], skemas_in[source], table)

    for destination in range(len(SOURCE_FILE_UPLOAD)):
        write_table(SOURCE_FILE_UPLOAD[destination], skema_table_out, table)
        gstorage.upload_file(
            BUCKET_NAME_UPLOAD,
            SOURCE_FILE_UPLOAD[destination],
            DESTINATION_FILE_UPLOAD[destination]
        )


if __name__ == '__main__':
    main()
