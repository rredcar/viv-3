import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

class MySQLConnection:

    def  __init__(self, port, host, database, user, password, rebuild_db=False):
        self.user = user
        self.password = password
        self.database = database

        self.host = host
        self.port = port

        self.rebuild_db = rebuild_db
        self.connection = self.connect()

        session = sessionmaker(
            bind=self.connection.engine,
            autocommit=True,
            autoflush=True,
            enable_baked_queries = False,
            expire_on_commit=True
        )
        self.session = session()

    def get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database if db_created else ""}',
            encoding='utf-8',
        )
        return engine.connect()

    def connect(self):
        connection = self.get_connection()
        if self.rebuild_db:
            connection.execute(text(f'DROP DATABASE IF EXISTS {self.database}'))
            connection.execute(text(f'CREATE DATABASE {self.database}'))
        connection.close()  # Закрываем старое соединение
        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8mb4'
        )
        return self.engine.connect()

    def execute_query(self, query):
        res = self.connection.execute(text(query))
        return res
