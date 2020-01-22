from google.cloud import bigquery
from bq_profile.profiler.bq_sql import aggregate


def test_bq_sql_aggregate_integer():
    project = 'project'
    dataset_id = 'dataset_id'
    table_id = 'table_id'
    name = 'name'
    i = 0
    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_ref = bigquery.TableReference(dataset_ref, table_id)
    f = bigquery.SchemaField('name', 'INTEGER')

    expected = ("SELECT 'name' name, 'INTEGER' type, COUNT(name) count, AVG(name) average, "
                'STDDEV_SAMP(name) std, CAST(MAX(name) AS STRING) max, CAST(MIN(name) AS '
                'STRING) min, CAST(APPROX_TOP_COUNT(name, 1)[ORDINAL(1)].value AS STRING) '
                'mode, COUNT(*) - COUNT(name) miss_count, SAFE_DIVIDE(COUNT(*) - COUNT(name), '
                'COUNT(*)) miss_rate, 0 miss_days, COUNT(DISTINCT name) unique_count, '
                'SAFE_DIVIDE(COUNT(DISTINCT name), COUNT(name)) unique_rate, '
                'CAST(APPROX_QUANTILES(name, 4)[ORDINAL(2)] AS STRING) quantile4_1, '
                'CAST(APPROX_QUANTILES(name, 4)[ORDINAL(3)] AS STRING) median, '
                'CAST(APPROX_QUANTILES(name, 4)[ORDINAL(4)] AS STRING) quantile4_3, '
                'CAST(APPROX_QUANTILES(name, 100)[ORDINAL(2)] AS STRING) quantile100_1, '
                'CAST(APPROX_QUANTILES(name, 100)[ORDINAL(100)] AS STRING) quantile100_99, '
                'COUNTIF(name >= 0) not_negatives, COUNTIF(name = 0) zeros, 0 empty_strings, '
                '0 ord FROM dataset_id.table_id')

    assert aggregate(f, table_ref, i, '""') == expected


def test_bq_sql_aggregate_numeric():
    project = 'project'
    dataset_id = 'dataset_id'
    table_id = 'table_id'
    name = 'name'
    i = 0
    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_ref = bigquery.TableReference(dataset_ref, table_id)
    f = bigquery.SchemaField('name', 'NUMERIC')

    expected = ("SELECT 'name' name, 'NUMERIC' type, COUNT(name) count, AVG(name) average, "
                'STDDEV_SAMP(name) std, CAST(MAX(name) AS STRING) max, CAST(MIN(name) AS '
                'STRING) min, CAST(APPROX_TOP_COUNT(name, 1)[ORDINAL(1)].value AS STRING) '
                'mode, COUNT(*) - COUNT(name) miss_count, SAFE_DIVIDE(COUNT(*) - COUNT(name), '
                'COUNT(*)) miss_rate, 0 miss_days, COUNT(DISTINCT name) unique_count, '
                'SAFE_DIVIDE(COUNT(DISTINCT name), COUNT(name)) unique_rate, '
                'CAST(APPROX_QUANTILES(name, 4)[ORDINAL(2)] AS STRING) quantile4_1, '
                'CAST(APPROX_QUANTILES(name, 4)[ORDINAL(3)] AS STRING) median, '
                'CAST(APPROX_QUANTILES(name, 4)[ORDINAL(4)] AS STRING) quantile4_3, '
                'CAST(APPROX_QUANTILES(name, 100)[ORDINAL(2)] AS STRING) quantile100_1, '
                'CAST(APPROX_QUANTILES(name, 100)[ORDINAL(100)] AS STRING) quantile100_99, '
                'COUNTIF(name >= 0) not_negatives, COUNTIF(name = 0) zeros, 0 empty_strings, '
                '0 ord FROM dataset_id.table_id')

    assert aggregate(f, table_ref, i, '""') == expected
