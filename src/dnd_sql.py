from sqlalchemy import create_engine
from pathlib import Path
from dotenv import load_dotenv
from os import getenv
import pandas as pd
import psycopg2
import os

folder_dir = os.path.join(Path(__file__).parents[0], 'data')

load_dotenv()
class PGSQL:
    __user = 'qxqdekzb'
    __password = 'PhAQn8YHzjFbSBOz9oRdohA5XXF1pYLB'
    __server = getenv("SERVER")
    __pg_con = psycopg2.connect(
        dbname=__user,
        user=__user,
        password=__password,
        host=__server
        )
    cur = __pg_con.cursor()
    #only used for the quick dump of the csvs's
    SQL_URL=getenv("SQ_URL")

    def create_tables(self, sql_filepath: str):
        start = self.create_file(sql_filepath)
        tables = start.split(';')
        for table in tables:
            try:
                print(table)
                self.cur.execute(table)
                self.__pg_con.commit()
            except psycopg2.ProgrammingError as msg:
                print(f'Command Skipped: {msg}')
    
    def upsert(self,csvpath,table):
        print(self.SQL_URL)
        #########build_temp_table to upsert from
        try:
            self.df = pd.read_csv(csvpath)
            engine = create_engine(self.SQL_URL)
            self.df.to_sql(table, con=engine, if_exists='replace', index=False)
        except psycopg2.ProgrammingError as msg:
                print(f'Command Skipped: {msg}')

    def query_db(self, sql_filepath: str):
        start = self.create_file(sql_filepath)
        queries = start.split(';')
        for query in queries:
            try:
                print(query)
                self.cur.execute(query)
                self.__pg_con.commit()
            except psycopg2.ProgrammingError as msg:
                msg
    @staticmethod

    def create_file(fpath: str):
        """ Open a file by filepath and apply it to an SQL table """
        with open(fpath, 'r') as f:
            sql_file = f.read()
            f.close()
        return sql_file


if __name__ == '__main__':
    p = PGSQL()
    #p.create_tables(r'C:\Users\Logan\Documents\GitHub\5e_Companion\src\create_tables.sql')
 
    p.upsert(f'{folder_dir}\monsters.csv','monsters')
    p.cur.close()
    p.upsert(f'{folder_dir}\monster_actions.csv','monster_actions')
    p.cur.close()
    p.upsert(f'{folder_dir}\monster_resists.csv','monster_resists')
    p.cur.close()
    p.upsert(f'{folder_dir}\monster_characteristics.csv','monster_characteristics')
    p.cur.close()
 
