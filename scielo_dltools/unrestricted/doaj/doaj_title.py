import argparse
import csv
import scielo_scholarly_data.standardizer as standardizer

from scielo_dltools.libs import gstorage


def read_table(arq, cols_to_read):
    table = []
    with open(arq) as doaj_in:
        csv_reader = csv.DictReader(doaj_in, delimiter=',')
        for row in csv_reader:
            rows = []
            for item in cols_to_read[:2]:
                rows.append(row.get(item))
            for item in cols_to_read[2:]:
                rows.append(row.get(item))
                rows.append(standardizer.journal_title_for_visualization(row.get(item)))
                rows.append(standardizer.journal_title_for_deduplication(row.get(item)))
            table.append(rows)
    return table


def write_table(arq, cols_to_write, table):
    with open(arq, 'w') as doaj_out:
        writer = csv.writer(doaj_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(cols_to_write)
        for rows in table:
            writer.writerow(rows)


def main():
    parser = argparse.ArgumentParser(description='Create a standardized titles file from data in Data Lake.')
    parser.add_argument('-bnd', action='store', dest='bucket_name_download',
                        required=True, help='Data Lake bucket to download.')
    parser.add_argument('-sfd', action='store', dest='source_file_download',
                        required=True, help='Source file to download.')
    parser.add_argument('-dfd', action='store', dest='destination_file_download',
                        required=True, help='Destination file to download.')
    parser.add_argument('-bnu', action='store', dest='bucket_name_upload',
                        required=True, help='Data Lake bucket to upload.')
    parser.add_argument('-sfu', action='store', dest='source_file_upload',
                        required=True, help='Source file to upload.')
    parser.add_argument('-dfu', action='store', dest='destination_file_upload',
                        required=True, help='Destination file to upload.')
    arguments = parser.parse_args()

    BUCKET_NAME_DOWNLOAD = arguments.bucket_name_download
    SOURCE_FILE_DOWNLOAD = arguments.source_file_download
    DESTINATION_FILE_DOWNLOAD = arguments.destination_file_download
    BUCKET_NAME_UPLOAD = arguments.bucket_name_upload
    SOURCE_FILE_UPLOAD = arguments.source_file_upload
    DESTINATION_FILE_UPLOAD = arguments.destination_file_upload

    gstorage.download_file(
        BUCKET_NAME_DOWNLOAD,
        SOURCE_FILE_DOWNLOAD,
        DESTINATION_FILE_DOWNLOAD
    )

    cols_to_read = [
        'Journal ISSN (print version)',
        'Journal EISSN (online version)',
        'Journal title',
        'Alternative title'
    ]

    cols_to_write = [
        'Journal ISSN (print version)',
        'Journal EISSN (online version)',
        'Journal title',
        'Journal title vis',
        'Journal title dep',
        'Alternative title',
        'Alternative title vis',
        'Alternative title dep']

    table = read_table(DESTINATION_FILE_DOWNLOAD, cols_to_read)
    write_table(SOURCE_FILE_UPLOAD, cols_to_write, table)

    gstorage.upload_file(
        BUCKET_NAME_UPLOAD,
        SOURCE_FILE_UPLOAD,
        DESTINATION_FILE_UPLOAD
    )


if __name__ == '__main__':
    main()
