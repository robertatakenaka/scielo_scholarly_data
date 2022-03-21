import argparse, textwrap
import json
import logging
import os
from argparse import RawTextHelpFormatter

from scielo_dltools.utils import requests_utils


# Read the DOAJ_LOG_FILE_PATH variable and create log file
doaj_log_file_path = os.environ["DOAJ_LOG_FILE_PATH"]

if not os.path.exists(doaj_log_file_path):
    os.makedirs(doaj_log_file_path)

log_path_file = os.path.join(doaj_log_file_path, 'doaj_getcsv.log.info.txt')

# Define log parameters
logging.basicConfig(filename=log_path_file, level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def getcsv(url, outdir, fname=None):
    # Read the variable User-Agent request header
    header = json.loads(os.environ['USER_AGENT'])

    # Check and create directory to save
    if not os.path.exists(outdir):
        msg=('creating directory %s' % (outdir))
        logger.info(msg)
        os.makedirs(outdir)

    # DOAJ Request
    try:
        msg = 'starting request'
        logger.info(msg)
        csv = requests_utils.request_url(url, {'User-Agent':'Mozilla/5.0'})
    except requests_utils.RequestUrlError as e:
        logger.error(e)
        return None

    # Slice the original file name from url requisited
    original_fname = csv.geturl().split('/')[-1]

    # Define output file name
    fname = fname or original_fname

    # Save CSV file
    try:
        with open(os.path.join(outdir, fname), 'wb') as f:
            msg = ('saving csv file %s in %s' % (fname, outdir))
            logger.info(msg)
            f.write(csv.read())
    except IOError as e:
        msg=('error while writing in %s' % (outdir))
        logger.info(msg)
        logger.error(e)
        return None

    # Log end of process
    msg = 'end of process'
    logging.info(msg)


def main():
    # Read DOAJ_URL variable
    url = os.environ['DOAJ_URL']

    parser = argparse.ArgumentParser(description=textwrap.dedent('''
Get journal metadata in CSV format from https://doaj.org.
It's mandatory to create the environment variables

    DOAJ URL:
    export DOAJ_URL="https://doaj.org/csv"

    The User-Agent request header:
    export USER_AGENT="{\\"User-Agent\\":\\"Mozilla/5.0\\"}"

    Defines log recording directory:
    export DOAJ_LOG_PATH="/tmp/"
    '''),
    formatter_class=RawTextHelpFormatter)

    parser.add_argument('-d', '--outdir', help='Directory to save the CSV file',
    required=True)

    parser.add_argument('-o', '--outfile', help='Optional CSV file name')

    args = parser.parse_args()

    getcsv(url, args.outdir, args.outfile)


if __name__ == '__main__':
    main()