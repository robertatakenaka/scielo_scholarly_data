import argparse
import csv
import scielo_scholarly_data.standardizer as standardizer

from scielo_dltools.libs import gstorage


def main():
    gstorage.download_file(
        'scielo-datalake-standardized',
        'doaj-journal-metadata/doaj-journal-metadata-latest/title.csv',
        'doaj_journals_title.csv'
    )
    gstorage.download_file(
        'scielo-datalake-standardized',
        'portal-issn/issns-scl_portal-issn_20210930/title.csv',
        'issn_journals_title.csv'
    )

    issn_keys_doaj = [
        'Journal ISSN (print version)'
    ]
    titles_keys_doaj = [
        'Journal title',
        'Alternative title',
        'journal_title_for_vis',
        'alternative_title_for_vis',
        'journal_title_for_dep',
        'alternative_title_for_dep'
    ]

    issn_keys_issn_portal = [
        'issn_l'
    ]
    titles_keys_issn_portal = [
        'key_title',
        'title_proper',
        'key_title_for_vis',
        'title_proper_for_vis',
        'key_title_for_dep',
        'title_proper_for_dep'
    ]

    data = []

    with open('doaj_journals_title.csv') as doaj_in:
        csv_reader = csv.DictReader(doaj_in, delimiter=',')
        for row in csv_reader:
            for issn in issn_keys_doaj:
                for title in titles_keys_doaj:
                    if row.get(title) != '':
                        rows = []
                        rows.append(row.get(issn))
                        rows.append(row.get(title))
                        rows.append('DOAJ')
                        rows.append(title)
                        rows.append('2021-10-14')
                        data.append(rows)

    with open('issn_journals_title.csv') as issn_in:
        csv_reader = csv.DictReader(issn_in, delimiter=',')
        for row in csv_reader:
            for issn in issn_keys_issn_portal:
                for title in titles_keys_issn_portal:
                    if row.get(title) != '':
                        rows = []
                        rows.append(row.get(issn))
                        rows.append(row.get(title))
                        rows.append('ISSN Portal')
                        rows.append(title)
                        rows.append('2021-10-14')
                        data.append(rows)

    with open('table_title.csv', 'w') as out:
        writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['issn_SciELO', 'title', 'source', 'label', 'date'])
        for rows in data:
            writer.writerow(rows)

    gstorage.upload_file(
        'scielo-datalake-gold',
        'table_title.csv',
        'tables/title.csv'
    )


if __name__ == '__main__':
    main()
