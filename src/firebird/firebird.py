import os
import sys
import warnings
import pandas as pd
from sqlalchemy import MetaData, Table, DDL, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import DropConstraint
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from firebird_conn import connection
warnings.filterwarnings("ignore")

class Firebird_Engine:
    def __init__(self, db_path: str, client_path: str):
        self.db_path = db_path
        self.client_path = client_path
        self.engine = connection(self.db_path, self.client_path)
        self.metadata = MetaData(bind=self.engine)
        try:
            with self.engine.connect():
                print(f"Successfully connected to database")
        except SQLAlchemyError:
            raise

    def DataFrame(self, query: str) -> pd.DataFrame:
        """DataFrame method receives a SQL query,
        connects to the database and returns the table as a list

        Args:
            query (str): SQL query

        Returns:
            pd.DataFrame: queried table
        """
        df = pd.read_sql(query, self.engine)
        return df


    def drop_constraint(self, table_name):
        table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
        if table is not None:
            for fk in table.foreign_key_constraints:
                drop_constraint_query = DropConstraint(fk)
                self.engine.execute(drop_constraint_query)


    def drop_all_tables(self):
        tables = self.DataFrame(
            '''WITH table_names AS (
                SELECT rdb$relation_name
                FROM rdb$relations
                WHERE rdb$view_blr IS NULL AND (rdb$system_flag IS NULL OR rdb$system_flag = 0)
               )
            SELECT * FROM table_names;'''
        )
        tables = [value.strip() for value in tables.iloc[:,0].values]
        for table in tables:
            self.drop_constraint(table)
        for table in tables:
            drop_table = Table(table, self.metadata, autoload=True, autoload_with=self.engine)
            drop_table.drop(self.engine)


    def drop_all_domains(self):
        domains = self.DataFrame(
            '''SELECT RDB$FIELD_NAME
               FROM RDB$FIELDS
               WHERE RDB$SYSTEM_FLAG = 0
               AND NOT RDB$FIELD_NAME STARTS WITH 'RDB$'
               AND NOT RDB$FIELD_NAME STARTS WITH 'SEC$'
               AND NOT RDB$FIELD_NAME STARTS WITH 'MON$';'''
        )
        domains = [value.strip() for value in domains.iloc[:,0].values]
        for domain in domains:
            drop_domain_query = DDL(f'DROP DOMAIN {domain}')
            self.engine.execute(drop_domain_query)


    def drop_all(self):
        self.drop_all_tables()
        self.drop_all_domains()


    def run_query(self, query):
        queries = [sql for sql in [s.strip() for s in query.split(";")] if sql !='']
        for single_query in queries:
            self.engine.execute(text(single_query))
