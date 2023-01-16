import os
import logging
from dotenv import load_dotenv
import psycopg2

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

#postgres db
BASE_NAME = os.getenv('BASE_NAME')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')

logging.basicConfig(filename='load_education.log', filemode='a', format = '%(asctime)s  %(message)s')

def database_connection(base_name=BASE_NAME, login=LOGIN, password=PASSWORD, host=HOST):
    try:
        connection = psycopg2.connect(dbname=base_name, user=login, password=password, host=host)
        return connection
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Ошибка при работе с PostgreSQL: {error}")
        raise SystemExit(error)

def insert_data_to_table(connection, parsed_data, table_name, models_fields, clear=True):
    try:
        with connection:
            with connection.cursor() as cursor:
                if parsed_data:
                    if clear:
                        query = "TRUNCATE " + table_name + ";"
                        cursor.execute(query)
                    for data_row in parsed_data:
                        query = f"""INSERT INTO {table_name} {models_fields} VALUES {data_row};"""
                        cursor.execute(query)
                    logging.error(f"Данные загружены в таблицу {table_name}")
                    #количество данных в таблице
                    query = f"SELECT count(*) FROM {table_name};"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    logging.error(f"В таблицк {result} записей")
                else:
                    query = f"""SELECT * FROM {table_name} ORDER BY pk DESC LIMIT 1;"""
                    cursor.execute(query)
                    result = cursor.fetchall()
                    logging.error(f"Новые данные не загружены. Последняя старая запись в таблице {result}")
    except Exception as exception:
        logging.error(f"insert_data_to_table exception {exception}")
        raise SystemExit(exception)