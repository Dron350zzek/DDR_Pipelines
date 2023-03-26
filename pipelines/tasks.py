from pipelines.dbwork import *

class BaseTask:
    """Base Pipeline Task"""

    def run(self):
        raise RuntimeError('Do not run BaseTask!')

    def short_description(self):
        pass

    def __str__(self):
        task_type = self.__class__.__name__
        return f'{task_type}: {self.short_description()}'


class CopyToFile(BaseTask):
    """Copy table data to CSV file"""

    def __init__(self, table, output_file, connection = 'db.db'):
        self.table = table
        self.output_file = output_file
        self.connection = connection

    def short_description(self):
        return f'{self.table} -> {self.output_file}'

    def run(self):
        save(self.output_file, self.table, self.connection)
        print(f"Copy table `{self.table}` to file `{self.output_file}`")


class LoadFile(BaseTask):
    """Load file to table"""

    def __init__(self, table, input_file, connection='db.db'):
        self.table = table
        self.input_file = input_file
        self.connection = connection

    def short_description(self):
        return f'{self.input_file} -> {self.table}'

    def run(self):
        load(self.input_file, self.table, self.connection)
        print(f"Load file `{self.input_file}` to table `{self.table}`")


class RunSQL(BaseTask):
    """Run custom SQL query"""

    def __init__(self, sql_query, title=None, connection='db.db'):
        self.title = title
        self.sql_query = sql_query
        self.connection = connection

    def short_description(self):
        return f'{self.title}'

    def run(self):
        execSQL(self.sql_query, connection=self.connection)
        print(f"Run SQL ({self.title}):\n{self.sql_query}")

class CTAS(BaseTask):
    """SQL Create Table As Task"""

    def __init__(self, table, sql_query, title=None, connection='db.db'):
        self.table = table
        self.sql_query = sql_query
        self.title = title or table
        self.connection = connection

    def short_description(self):
        return f'{self.title}'

    def run(self):
        create(self.table, self.sql_query, connection=self.connection)
        print(f"Create table `{self.table}` as SELECT:\n{self.sql_query}")
