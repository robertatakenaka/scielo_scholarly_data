from google.cloud import bigquery
from google.api_core.exceptions import Conflict, Forbidden


def _connect():
    return bigquery.Client()


def _generate_dataset_id(project_name, dataset_name):
    return '{}.{}'.format(project_name, dataset_name)


def _generate_table_id(project_name, dataset_name, table_id):
    return '{}.{}.{}'.format(project_name, dataset_name, table_id)


def create_dataset(dataset_name):
    bq_client = _connect()
    dataset_id = _generate_dataset_id(bq_client.project, dataset_name)

    try:
        ds = bq_client.create_dataset(dataset_id)
    except Forbidden:
        print('Access denied')
    except Conflict:
        print('Dataset {} already exists'.format(dataset_id))
    else:
        print('Dataset {} created with success'.format(dataset_id))
        return ds


def load_table_from_uri(uri, dataset_name, table_name):
    bq_client = _connect()

    table_id = _generate_table_id(
        bq_client.project,
        dataset_name,
        table_name
    )

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )

    print('Loading table...')
    job = bq_client.load_table_from_uri(
        [uri],
        table_id,
        job_config=job_config
    )

    job.result()

    table = bq_client.get_table(table_id)
    print(
        'Loaded {} rows and {} columns to {}'.format(
            table.num_rows,
            len(table.schema),
            table_id
        )
    )
    return table
