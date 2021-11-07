import unittest

from scielo_dltools.utils.bucket_utils import (
    get_bucket_name,
    get_directory,
    get_file_name,
)


class TestBucketUtils(unittest.TestCase):

    def test_get_bucket_name_no_file_informed(self):
        gspath_raw = 'gs://scielo-datalake-raw/index/cwts/journal-indicators/'
        self.assertEqual(get_bucket_name(gspath_raw), 'scielo-datalake-raw')

        gspath_gold = 'gs://scielo-datalake-gold/index/cwts/journal-indicators/'
        self.assertEqual(get_bucket_name(gspath_gold), 'scielo-datalake-gold')

    def test_get_bucket_name_file_informed(self):
        gspath_raw = 'gs://scielo-datalake-raw/index/cwts/journal-indicators/CWTS Journal Indicators April 2021.xlsx'
        self.assertEqual(get_bucket_name(gspath_raw), 'scielo-datalake-raw')

        gspath_std = 'gs://scielo-datalake-standardized/index/scimago/journal-indicators/scimago_d_2006.csv'
        self.assertEqual(get_bucket_name(gspath_std), 'scielo-datalake-standardized')

    def test_get_bucket_name_invalid(self):
        gspath = 'g://scielo-datalake-raw/index/doaj/journal-metadata.csv'
        self.assertIsNone(get_bucket_name(gspath))

    def test_get_directory_no_file_informed(self):
        gspath = 'gs://scielo-datalake-raw/index/portal-issn/'
        self.assertEqual(get_directory(gspath), 'index/portal-issn')

    def test_get_directory_file_informed(self):
        gspath = 'gs://scielo-datalake-standardized/index/portal-issn/journal-metadata-scl.jsonl'
        self.assertEqual(get_directory(gspath), 'index/portal-issn')

    def test_get_directory_invalid(self):
        gspath = '://scielo-datalake-raw/index/scielo/'
        self.assertIsNone(get_directory(gspath))

    def test_get_file_name(self):
        gspath = 'gs://scielo-datalake-raw/index/scimago/journal-indicators/scimago_d_2004.csv'
        self.assertEqual(get_file_name(gspath), 'scimago_d_2004.csv')

    def test_get_file_name_without_extension(self):
        gspath = 'gs://scielo-datalake-raw/index/scimago/journal-indicators/scimago_d_2004'
        self.assertEqual(get_file_name(gspath), 'scimago_d_2004')

    def test_get_file_name_separate_extension(self):
        gspath_no_filo_informed = 'gs://scielo-datalake-raw/index/scielo/scielo-analytics-reports/'
        self.assertEqual(get_file_name(gspath_no_filo_informed, separate_extension=True), ('', ''))

        gspath_file_informed = 'gs://scielo-datalake-gold/index/scimago/journal-indicators/scimago_d_2005.csv'
        self.assertEqual(get_file_name(gspath_file_informed, separate_extension=True), ('scimago_d_2005', '.csv'))
