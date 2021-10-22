import csv
import json
import scielo_scholarly_data.standardizer as standardizer

from scielo_dltools.libs import gstorage


def clear(value):
    if type(value) == list:
        return value[0]
    else:
        return ''


def read_json(arq, attribs_to_read, table):
    registros = []
    for line in open(arq, 'r'):
        registros.append(json.loads(line))
    for row in registros:
        rows = []
        for item in attribs_to_read[:2]:
            rows.append(clear(row.get(item)))
        for item in attribs_to_read[2:]:
            rows.append(clear(row.get(item)))
            rows.append(standardizer.journal_title_for_visualization(clear(row.get(item))))
            rows.append(standardizer.journal_title_for_deduplication(clear(row.get(item))))
        table.append(rows)


def write_table(arq, cols_to_write, table):
    with open(arq, 'w') as out:
        writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(cols_to_write)
        for rows in table:
            writer.writerow(rows)


def main():
    BUCKET_NAME_DOWNLOAD = 'scielo-datalake-raw'
    SOURCE_FILE_DOWNLOAD = 'index/portal-issn/journal-metadata-scl.jsonl'
    DESTINATION_FILE_DOWNLOAD = '/home/luciano/nuvem/Dropbox/scielo/data_lake/journal-metadata-scl.jsonl'
    BUCKET_NAME_UPLOAD = 'scielo-datalake-standardized'
    SOURCE_FILE_UPLOAD = '/home/luciano/nuvem/Dropbox/scielo/data_lake/journal-metadata-scl.csv'
    DESTINATION_FILE_UPLOAD = 'index/issn/journal-titles.csv'

    gstorage.download_file(
        BUCKET_NAME_DOWNLOAD,
        SOURCE_FILE_DOWNLOAD,
        DESTINATION_FILE_DOWNLOAD
    )

    attribs_to_read = [
        'issn',
        'issn_l',
        'key_title',
        'title_proper'
    ]

    cols_to_write = [
        'issn',
        'issn_l',
        'key_title',
        'key_title vis',
        'key_title dep',
        'title_proper',
        'title_proper vis',
        'title_proper dep']

    table = []

    read_json(DESTINATION_FILE_DOWNLOAD, attribs_to_read, table)
    write_table(SOURCE_FILE_UPLOAD, cols_to_write, table)

    gstorage.upload_file(
        BUCKET_NAME_UPLOAD,
        SOURCE_FILE_UPLOAD,
        DESTINATION_FILE_UPLOAD
    )


if __name__ == '__main__':
    main()
