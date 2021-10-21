import csv
import scielo_scholarly_data.standardizer as standardizer

from scielo_dltools.libs import gstorage


def read_table(arq, cols_to_read, table):
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


def write_table(arq, cols_to_write, table):
    with open(arq, 'w') as doaj_out:
        writer = csv.writer(doaj_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(cols_to_write)
        for rows in table:
            writer.writerow(rows)


def main():
    BUCKET_NAME_DOWNLOAD = 'scielo-datalake-raw'
    SOURCE_FILE_DOWNLOAD = 'index/doaj/journal-metadata.csv'
    DESTINATION_FILE_DOWNLOAD = '/home/luciano/nuvem/Dropbox/scielo/data_lake/journal-metadata.csv'
    BUCKET_NAME_UPLOAD = 'scielo-datalake-standardized'
    SOURCE_FILE_UPLOAD = '/home/luciano/nuvem/Dropbox/scielo/data_lake/journal-titles.csv'
    DESTINATION_FILE_UPLOAD = 'index/doaj/journal-titles.csv'

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

    table = []

    read_table(DESTINATION_FILE_DOWNLOAD, cols_to_read, table)
    write_table(SOURCE_FILE_UPLOAD, cols_to_write, table)

    gstorage.upload_file(
        BUCKET_NAME_UPLOAD,
        SOURCE_FILE_UPLOAD,
        DESTINATION_FILE_UPLOAD
    )


if __name__ == '__main__':
    main()
