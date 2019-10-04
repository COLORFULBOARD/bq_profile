import pandas as pd
import pandas_profiling as pdp


class Profiler:
    def __init__(self, project, sql, *args, **kwargs):
        self.project = project
        try:
            self.sql = open(sql).read()
        except:
            self.sql = sql
        self.df = None
        self.profile = None

    def get_stats(self):
        raise NotImplementedError()

    def to_file(self, filename):
        raise NotImplementedError()

    def to_bq(self, table, disposition):
        raise NotImplementedError()

    def show(self):
        print(self.profile)


class DescribeProfiler(Profiler):
    def __init__(self, project, sql, errors, *args, **kwargs):
        super().__init__(project, sql)
        self.errors = errors

    def get_stats(self):
        self.df = pd.read_gbq(self.sql, project_id=self.project, dialect="standard")
        self.profile = self.df.describe(include="all")

    def to_file(self, filename):
        self.profile.to_csv(filename, index=False)

    def to_bq(self, table, disposition):
        data = self.profile.T.reset_index()
        data = data.rename(
            columns={'index': 'name', '25%': 'quantile4_1', '50%': 'median', '75%': "quantile4_3"})
        data.to_gbq(table, project_id=self.project, if_exists=disposition)


class PandasProfiler(Profiler):
    def __init__(self, project, sql, errors, *args, **kwargs):
        super().__init__(project, sql)
        self.errors = errors

    def get_stats(self):
        self.df = pd.read_gbq(self.sql, project_id=self.project, dialect="standard")
        self.profile = pdp.ProfileReport(self.df)

    def to_file(self, filename):
        self.profile.to_file(filename)
