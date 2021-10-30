import argparse
import csv
import scielo_scholarly_data.standardizer as standardizer
import tempfile

from scielo_dltools.libs import gstorage


def read_table(arq, cols_to_read):
    table = []
    with open(arq) as data:
        for row in csv.DictReader(data, delimiter=','):
            cols = [
                standardizer.journal_issn(row.get(cols_to_read[0]), use_issn_validator=True),
                row.get(cols_to_read[1]),
                standardizer.journal_title_for_visualization(row.get(cols_to_read[1])),
                standardizer.journal_title_for_deduplication(row.get(cols_to_read[1]))
            ]
            if cols not in table:
                table.append(cols)
    return table


def write_table(arq, cols_to_write, table):
    with open(arq, 'w') as data:
        writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(cols_to_write)
        for cols in table:
            writer.writerow(cols)


def main():
    parser = argparse.ArgumentParser(description='Create a standardized titles file from data in Data Lake.')
    parser.add_argument('-d', '--file_to_download', dest='path_file_to_download', required=True,
                        help='Path file to download from Data Lake.')
    parser.add_argument('-u', '--file_to_upload', dest='path_file_to_upload', required=True,
                        help='Path file to upload to Data Lake.')
    arguments = parser.parse_args()

    BUCKET_NAME_DOWNLOAD = arguments.path_file_to_download.split('/')[0]
    SOURCE_FILE_DOWNLOAD = '/'.join(arguments.path_file_to_download.split('/')[1:])
    DESTINATION_FILE_DOWNLOAD = str(tempfile.TemporaryFile())
    BUCKET_NAME_UPLOAD = arguments.path_file_to_upload.split('/')[0]
    SOURCE_FILE_UPLOAD = DESTINATION_FILE_DOWNLOAD
    DESTINATION_FILE_UPLOAD = '/'.join(arguments.path_file_to_upload.split('/')[1:])

    gstorage.download_file(
        BUCKET_NAME_DOWNLOAD,
        SOURCE_FILE_DOWNLOAD,
        DESTINATION_FILE_DOWNLOAD
    )

    cols_to_read = [
        'ISSN SciELO',
        'title at SciELO'
    ]

    cols_to_write = [
        'ISSN SciELO',
        'title at SciELO',
        'title at SciELO vis',
        'title at SciELO dep'
    ]

    table = read_table(DESTINATION_FILE_DOWNLOAD, cols_to_read)
    write_table(SOURCE_FILE_UPLOAD, cols_to_write, table)

    gstorage.upload_file(
        BUCKET_NAME_UPLOAD,
        SOURCE_FILE_UPLOAD,
        DESTINATION_FILE_UPLOAD
    )


if __name__ == '__main__':
    main()
