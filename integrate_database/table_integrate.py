import pandas as pd
import json
import pprint
import string
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker

import sys, os
# 상위 경로 module 호출을 위해 표시
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import db_setting
from se_shoplinker_tbl import se_shoplinker_tbl

# module에 입력한 setting 정보 읽어오기
def get_setting(env):
    config = {}
    for setting in dir(db_setting):
        if setting.islower() and setting.isalpha():
            config[setting] = getattr(db_setting, setting)

    return config.get(env)


class TableIntegrate():
    def __init__(self, env, table_name):
        self.db_setting = db_setting
        self.env        = env
        self.table_name = table_name
        if table_name in se_shoplinker_tbl:
            setting = get_setting(env).get('main')
        else:
            setting = get_setting(env).get('cust')

        self.engine = create_engine('mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}?charset=utf8mb4'.format(**setting), pool_recycle=120, pool_size=3, max_overflow=20, echo=False, echo_pool=False)

    def get_integrate_tbl_data(self):
        where_condition = ''
        with self.engine.connect() as connection:
            sql_query = f"select * from {self.table_name} {where_condition};"
            dataframe = pd.read_sql(sql_query, connection)
            return dataframe

    # DataFrame.to_sql(name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None)
    def set_integrate_tbl_data(self, insert_tbl):
        df = self.table_columns_integrate_matching()

        # match된 dataframe database에 insert
        with self.engine.connect() as connection:
            df.to_sql(name=insert_tbl, con=connection, if_exists='append', index=False)

    # data match processing
    def table_columns_integrate_matching(self, df):
        ...

    # excel_column index => alphabet
    def get_column_name(self, index):
        column_name = ""
        while index >= 0:
            remainder = index % 26
            column_name = f"{string.ascii_uppercase[remainder]}{column_name}"
            index = (index // 26) - 1
        return column_name.lower()
