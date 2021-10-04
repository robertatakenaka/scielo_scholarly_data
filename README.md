# SciELO Data Lake Tools
SciELO Data Lake Tools is a repository which contains a set of tools to insert data in the data lake or get data from the data lake.


# Google Cloud Plataform Tools

## Installation

```shell
virtualenv -p python3.6 .venv
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
