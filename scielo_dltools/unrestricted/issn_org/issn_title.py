import csv
import json
import scielo_scholarly_data.standardizer as standardizer

from scielo_dltools.libs import gstorage


def clear(value):
    if type(value) == list:
        return value[0]
    else:
        return ''


gstorage.download_file(
    'scielo-datalake-raw',
    'portal-issn/issns-scl_portal-issn_20210930.jsonl',
    'issn_journals_title.jsonl'
)

issn_keys = ['issn', 'issn_l']
title_keys = ['key_title', 'title_proper']
vis_keys = ['key_title_for_vis', 'title_proper_for_vis']
dep_keys = ['key_title_for_dep', 'title_proper_for_dep']

registros = []
for line in open('issn_journals_title.jsonl', 'r'):
    registros.append(json.loads(line))

data = []
for row in registros:
    rows = []
    for item in issn_keys:
        rows.append(clear(row.get(item)))
    for item in title_keys:
        rows.append(clear(row.get(item)))
    for item in title_keys:
        rows.append(standardizer.journal_title_for_visualization(clear(row.get(item))))
    for item in title_keys:
        rows.append(standardizer.journal_title_for_deduplication(clear(row.get(item))))
    data.append(rows)

with open('issn_journals_title.csv', 'w') as doaj_out:
    writer = csv.writer(doaj_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(issn_keys + title_keys + vis_keys + dep_keys)
    for rows in data:
        writer.writerow(rows)

gstorage.upload_file(
    'scielo-datalake-standardized',
    'issn_journals_title.csv',
    'portal-issn/issns-scl_portal-issn_20210930/title.csv'
)
