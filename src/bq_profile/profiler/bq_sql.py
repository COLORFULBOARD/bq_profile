from contextlib import contextmanager
from uuid import uuid4

import pandas as pd
from google.cloud import bigquery

from .basic import Profiler


class SqlProfiler(Profiler):
    def __init__(self, project, sql, *args, **kwargs):
        super().__init__(project, sql)
        self.client = bigquery.Client(project=project)

    def get_stats(self):
        with tmp_table(self.client, self.sql) as table_ref:
            self.profile = get_stats(self.client, self.project, table_ref)

    def to_file(self, filename):
        self.profile.to_csv(filename, index=False)

    def to_bq(self, table, disposition):
        self.profile.to_gbq(table, project_id=self.project, if_exists=disposition)


@contextmanager
def tmp_table(client, sql):
    dataset_id = f"tmp_dataset_{uuid4().hex}"
    table_id = f"tmp_{uuid4().hex}"
    job_config = bigquery.QueryJobConfig()
    dataset_ref = client.dataset(dataset_id)
    client.create_dataset(bigquery.Dataset(dataset_ref))
    job_config.destination = dataset_ref.table(table_id)
    table_ref = None
    try:
        query_job = client.query(sql, location="US", job_config=job_config)
        query_job.result()
        table_ref = dataset_ref.table(table_id)
        yield table_ref
    finally:
        try:
            client.delete_table(table_ref)
        except:
            pass
        client.delete_dataset(client.dataset(dataset_id))


def aggregate(f, table_ref, i, empty_string):
    return (
        f"SELECT"
        f" '{f.name}' name,"
        f" '{f.field_type}' type,"
        f" COUNT({f.name}) count,"
        f" {f'AVG({f.name})' if f.field_type in ('INTEGER', 'FLOAT', 'NUMERIC') else 'null'} average,"
        f" {f'STDDEV_SAMP({f.name})' if f.field_type in ('INTEGER', 'FLOAT', 'NUMERIC') else 'null'} std,"
        f" CAST(MAX({f.name}) AS STRING) max,"
        f" CAST(MIN({f.name}) AS STRING) min,"
        f" CAST(APPROX_TOP_COUNT({f.name}, 1)[ORDINAL(1)].value AS STRING) mode,"
        f" COUNT(*) - COUNT({f.name}) miss_count,"
        f" SAFE_DIVIDE(COUNT(*) - COUNT({f.name}),"
        f" COUNT(*)) miss_rate,"
        f" {f'DATE_DIFF(MAX({f.name}), MIN({f.name}), DAY) + 1 - COUNT(DISTINCT {f.name})' if f.field_type == 'DATE' else '0'} miss_days,"
        f" COUNT(DISTINCT {f.name}) unique_count,"
        f" SAFE_DIVIDE(COUNT(DISTINCT {f.name}), COUNT({f.name})) unique_rate,"
        f" {f'CAST(APPROX_QUANTILES({f.name}, 4)[ORDINAL(2)] AS STRING)' if f.field_type not in ('STRUCT', 'ARRAY') else 'null'} quantile4_1,"
        f" {f'CAST(APPROX_QUANTILES({f.name}, 4)[ORDINAL(3)] AS STRING)' if f.field_type not in ('STRUCT', 'ARRAY') else 'null'} median,"
        f" {f'CAST(APPROX_QUANTILES({f.name}, 4)[ORDINAL(4)] AS STRING)' if f.field_type not in ('STRUCT', 'ARRAY') else 'null'} quantile4_3,"
        f" {f'CAST(APPROX_QUANTILES({f.name}, 100)[ORDINAL(2)] AS STRING)' if f.field_type not in ('STRUCT', 'ARRAY') else 'null'} quantile100_1,"
        f" {f'CAST(APPROX_QUANTILES({f.name}, 100)[ORDINAL(100)] AS STRING)' if f.field_type not in ('STRUCT', 'ARRAY') else 'null'} quantile100_99,"
        f" {f'COUNTIF({f.name} >= 0)' if f.field_type in ('INTEGER', 'FLOAT', 'NUMERIC') else '0'} not_negatives,"
        f" {f'COUNTIF({f.name} = 0)' if f.field_type in ('INTEGER', 'FLOAT', 'NUMERIC') else '0'} zeros,"
        f" {f'COUNTIF({f.name} = {empty_string})' if f.field_type == 'STRING' else '0'} empty_strings,"
        f" {i} ord FROM {table_ref.dataset_id}.{table_ref.table_id}"
    )


def get_stats(client, project, table_ref, empty_string='""', max_size=50):
    schema = client.get_table(f"{table_ref.dataset_id}.{table_ref.table_id}").schema
    num_columns = len(schema)
    num_repeats = -(-num_columns // max_size)

    sqls = (
        " UNION ALL ".join(
            aggregate(f, table_ref, j * max_size + i, empty_string)
            for i, f in enumerate(schema[j * max_size : min(num_columns, (j + 1) * max_size)])
        )
        + " ORDER BY ord;"
        for j in range(num_repeats)
    )
    dfs = (pd.read_gbq(sql, project_id=project, dialect="standard") for sql in sqls)
    return pd.concat(dfs)
