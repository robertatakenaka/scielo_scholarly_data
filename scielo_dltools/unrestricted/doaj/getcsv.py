import argparse
import logging
import os

from scielo_dltools.utils import requests_utils


# Check the real path and create log directory
dir_path = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(dir_path + '/logs'):
    os.makedirs(dir_path + '/logs')

# Define log parameters
log_path_file = dir_path + '/logs/getcsv.log.info.txt'

logging.basicConfig(filename=log_path_file,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def getcsv(url, headers, outdir, fname=None):
    # Check and create directory to save
    if not os.path.exists(outdir):
        msg=('creating directory ', outdir)
        logger.info(msg)
        os.makedirs(outdir)

    # DOAJ Request
    try:
        msg = 'starting request'
        logger.info(msg)
        csv = requests_utils.request_url(url, headers)
    except requests_utils.RequestUrlError as e:
        logger.error(e)
        return None

    # Slice the original file name from url requisited
    original_fname = csv.geturl().split('/')[-1]

    # Define output file name
    fname = fname or original_fname

    # Save CSV file
    try:
        with open(outdir + '/' + fname, 'wb') as f:
            msg = ('saving csv file %s in %s' % (fname, outdir))
            logger.info(msg)
            f.write(csv.read())
    except IOError as e:
        msg=('error while writing', outdir)
        logger.info(msg)
        logger.error(e)
        return None

    # Log end of process
    msg = ('end of process')
    logging.info(msg)



def main():
    # DOAJ URL and Headers
    url = 'https://doaj.org/csv'
    headers = {'User-Agent':'Mozilla/5.0'}

    parser = argparse.ArgumentParser(
        description='Get journal metadata in CSV format from https://doaj.org')

    parser.add_argument('-d', '--outdir',
        default=os.path.expanduser('~') + '/doaj_csv/',
        help='Optional directory to save the CSV file. Default: ~/doaj_csv/' )

    parser.add_argument('-o', '--outfile', help='Optional CSV file name ')

    args = parser.parse_args()

    getcsv(url, headers, args.outdir, args.outfile)


if __name__ == '__main__':
    main()
