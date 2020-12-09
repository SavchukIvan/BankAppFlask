import psycopg2

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from dao.credentials import *
# from credentials import *


class PostgresDb:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                connection = psycopg2.connect(host=HOST,
                                              database=DATABASE,
                                              user=USER,
                                              password=PASSWORD)
                cursor = connection.cursor()

                # execute a statement
                print('PostgreSQL database version:')
                cursor.execute('SELECT version()')

                # display the PostgreSQL database server version
                db_version = cursor.fetchone()
                print(db_version)

                engine = create_engine(DB_URI)

                Session = sessionmaker(bind=engine)
                session = Session()

                PostgresDb._instance.sqlalchemy_session = session
                PostgresDb._instance.sqlalchemy_engine = engine
                PostgresDb._instance.connection = connection
                PostgresDb._instance.cursor = cursor

            except Exception as error:
                print('Error: connection not established {}'.format(error))

        return cls._instance

    def __init__(self):
        postgre_connection_string = DB_URI
        engine = create_engine(postgre_connection_string)

        Session = sessionmaker(bind=engine)
        session = Session()

        self.sqlalchemy_session = session
        self.sqlalchemy_engine = engine
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def execute(self, query):
        '''
        Функція, що дозволяє робити
        запити з бд
        '''
        try:
            self.cursor.execute(query)
            result = self.cursor
            self.connection.commit()
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result

    def __del__(self):
        self.sqlalchemy_session.close()


if __name__ == "__main__":
    db = PostgresDb()
    # print('Час у вас за вікном:')
    # print(db.execute('''SELECT now()''')[0])
