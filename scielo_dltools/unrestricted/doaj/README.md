# DOAJ

This module gets journal metadata in CSV format from https://doaj.org


### Requirements
Python >= 3.7


### Environment variables

Inform the DOAJ URL:

`export DOAJ_URL="https://doaj.org/csv"`


Defines log recording directory:

`export DOAJ_LOG_PATH="/tmp/"`


### Usage

__Show help__

```bash
python3 scielo_dltools/unrestricted/doaj/getcsv.py -h
```

output:
```
usage: getcsv.py [-h] [-d OUTDIR] [-o OUTFILE]
Get journal metadata in CSV format from https://doaj.org

optional arguments:
  -h, --help            show this help message and exit

  -d OUTDIR, --outdir OUTDIR
                        Directory to save the CSV file. Required.
  -o OUTFILE, --outfile OUTFILE
                        Optional CSV file name
```
__Example__

```bash
python3 scielo_dltools/unrestricted/doaj/getcsv.py -d ~/doaj_csv/
```

__Log File__

Check the log file "getcsv.log.info.txt" in the directory defined in DOAJ_LOG_PATH variable
