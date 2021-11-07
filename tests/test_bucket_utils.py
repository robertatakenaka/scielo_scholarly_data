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
