import argparse
from tempfile import NamedTemporaryFile

from google.cloud import storage
from profiler import DescribeProfiler, PandasProfiler, SqlProfiler

PROFILER = {
    "describe": DescribeProfiler,
    "pandas-profiling": PandasProfiler,
    "sql": SqlProfiler
}


def main(args):
    profiler = PROFILER[args.mode](**vars(args))
    profiler.get_stats()
    if args.output_table:
        profiler.to_bq(args.output_table, args.disposition)
    elif args.output.startswith("gs://"):
        with NamedTemporaryFile("w", delete=False) as f:
            profiler.to_file(f.name)
        upload_to_gcs(args.output, f.name, args.project)
    elif args.output:
        profiler.to_file(args.output)
    else:
        profiler.show()


def upload_to_gcs(uri, filename, project):
    client = storage.Client(project=project)
    bucket_name, blob_name = uri[5:].split("/", 1)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sql", required=True)
    parser.add_argument("--project", dest="project", required=True, help="gcp project id")
    parser.add_argument("--mode", default="basic", choices=PROFILER.keys())
    parser.add_argument("--output", default="", help="path or gs://... for output HTML")
    parser.add_argument("--output-table", dest="output_table", default=None)
    parser.add_argument("--disposition", default="fail", choices=("fail", "replace", "append"))
    args, _ = parser.parse_known_args()
    main(args)
