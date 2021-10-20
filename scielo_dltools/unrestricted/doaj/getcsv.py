import argparse
import os
import urllib.request


URL = 'https://doaj.org/csv'


def getcsv(url, outdir, fname=None):
    # Check and create directory to save
    if not os.path.exists(outdir):
        print('Creating directory', outdir, 'to save')
        os.makedirs(outdir)

    # Request to DOAJ
    try:
        req = urllib.request.Request(URL, headers={'User-Agent':'Mozilla/5.0'})
        print('Downloading CSV file')
        csv = urllib.request.urlopen(req)
    except Exception as e:
        print(e)
        sys.exit()

    # Slice the original file name from url requisited
    original_fname = csv.geturl().split('/')[-1]

    # Define output file name
    fname = fname or original_fname

    # Save CSV file
    with open(outdir + '/' + fname, 'wb') as f:
        print('Saving file as', fname, 'in', outdir, 'directory')
        f.write(csv.read())


def main():
    parser = argparse.ArgumentParser(
        description='Get journal metadata in CSV format from https://doaj.org')

    parser.add_argument('-d', '--outdir',
        default ='output',
        help='Optional directory to save the CSV file. Default: output' )

    parser.add_argument('-o', '--outfile',
                        help='Optional CSV file name ')

    args = parser.parse_args()

    if args.outdir:
        DOWNLOAD_DIR = args.outdir

    if args.outfile is None:
        getcsv(URL, DOWNLOAD_DIR)
    else:
        getcsv(URL, DOWNLOAD_DIR, args.outfile)


if __name__ == '__main__':
    main()
