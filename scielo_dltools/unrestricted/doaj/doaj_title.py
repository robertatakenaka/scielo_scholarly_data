import csv
import scielo_scholarly_data.standardizer as standardizer

from scielo_dltools.libs import gstorage

gstorage.download_file(
    'scielo-datalake-raw',
    'doaj-journal-metadata/doaj-journal-metadata-latest.csv',
    'doaj_journals.csv'
)

issn_keys = ['Journal ISSN (print version)', 'Journal EISSN (online version)']
title_keys = ['Journal title', 'Alternative title']
vis_keys = ['journal_title_for_vis', 'alternative_title_for_vis']
dep_keys = ['journal_title_for_dep', 'alternative_title_for_dep']

with open('doaj_journals.csv') as doaj_in:
    csv_reader = csv.DictReader(doaj_in, delimiter=',')
    data = []
    for row in csv_reader:
        rows = []
        for item in issn_keys:
            rows.append(row.get(item))
        for item in title_keys:
            rows.append(row.get(item))
        for item in title_keys:
            rows.append(standardizer.journal_title_for_visualization(row.get(item)))
        for item in title_keys:
            rows.append(standardizer.journal_title_for_deduplication(row.get(item)))
        data.append(rows)

with open('doaj_journals_title.csv', 'w') as doaj_out:
    writer = csv.writer(doaj_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(issn_keys + title_keys + vis_keys + dep_keys)
    for rows in data:
        writer.writerow(rows)

gstorage.upload_file(
    'scielo-datalake-standardized',
    'doaj_journals_title.csv',
    'doaj-journal-metadata/doaj-journal-metadata-latest/title.csv'
)
