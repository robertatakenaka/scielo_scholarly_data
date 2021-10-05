# SciELO Data Lake Tools
SciELO Data Lake Tools is a repository which contains a set of tools to insert data in the data lake or get data from the data lake.

# Google Cloud Plataform Tools

## Installation

```shell
virtualenv -p python3.9 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

`GOOGLE_APPLICATION_CREDENTIALS=/home/user/key.json`

## Usage

### Google Cloud BigQuery (gbq.py)

__Create dataset__
```shell
# python gpq.py create_dataset dataset_name
# example
python gbq.py create_dataset fapesp_report
```

__Load table from Google Cloud Storage__
```shell
# python gpq.py load_table_from_uri dataset_name uri table
# example
python gbq.py load_table_from_uri gs://scielo-datalake-raw/scielo-analytics/brazil/accesses-by-journals-2021-07-09.csv fapesp_report journal_collection
```

### Google Cloud Storage (gcs.py)

__Download data__
```shell
# python gstorage.py download BUCKET_NAME SOURCE_FILE DESTINATION_FILE
# example
python gstorage.py download scielo-datalake-raw pid-dates/pid-dates-2020-11-27.csv pid-dates.csv
```

__Upload data__
```shell
# python gstorage.py upload BUCKET_NAME SOURCE_FILE DESTINATION_FILE
# example
python gstorage.py upload scielo-datalake-standardized pid-dates.csv pid-dates/pid-dates.csv
```

__List bucket content__
```shell
# python gstorage.py upload BUCKET_NAME
# example
python gstorage.py list scielo-datalake-raw
```

__Rename file__
```shell
# python gstorage.py upload BUCKET_NAME SOURCE_FILE DESTINATION_FILE
# example 1
python gstorage.py rename scielo-datalake-raw pid-dates/pid-dates-2020-11-27.csv pid-dates/pid-dates-latest.csv
# example 2
python gstorage.py rename scielo-datalake-raw pid-dates/pid-dates-latest.csv pid-dates/pid-dates-2020-11-27.csv
```

__Get metadata__
```shell
# python gstorage.py metadata BUCKET_NAME SOURCE_FILE
# example
python gstorage.py metadata scielo-datalake-raw pid-dates/pid-dates-2020-11-27.csv
```

## Available buckets

- scielo-datalake-raw
- scielo-datalake-standardized
- scielo-datalake-gold
