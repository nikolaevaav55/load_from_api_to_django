#!/usr/bin/python3
from json import JSONDecodeError

from pydantic import BaseModel, ValidationError
import json
import psycopg2
import codecs
import sys
from psycopg2 import Error
import requests
from requests.auth import HTTPBasicAuth
import logging
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


#postgres db
BASE_NAME = os.getenv('BASE_NAME')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')

#API
CHISLENNOST_API_URL = os.getenv('CHISLENNOST_API_URL')
CHISLENNOST_VOST_I_OT_API_URL = os.getenv('CHISLENNOST_VOST_I_OT_API_URL')
API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')

#models
EDUCATION_THREE_TABLE = os.getenv('EDUCATION_THREE_TABLE')
EDUCATION_FIVE_TABLE = os.getenv('EDUCATION_FIVE_TABLE')

#json path
CHISLENNOST_JSON_PATH = './ftpjson/chislennost.json'
DYNAMICS_JSON_PATH = './ftpjson/chislennost_Otchis_i_vost.json'



EDUCATION_THREE_FIELDS = """
(   
    edu_code, 
    edu_name,
    edu_level,
    edu_form,
    number_bf,
    number_bff,
    number_br,
    number_brf,
    number_bm,
    number_bmf,
    number_p,
    number_pf,
    number_all,
    update_time,
    update_date
)
"""

EDUCATION_FIVE_FIELDS = """
(   
    edu_code,
    edu_name,
    edu_level,
    edu_form,
    number_out_perevod,
    number_to_perevod,
    number_res_perevod,
    number_exp_perevod,
    update_time,
    update_date
)
"""


class EducationThree(BaseModel): # www.dipacademy.ru/sveden/education/obr-3/(Информация о численности обучающихся)
    Код: str
    Специальность: str
    УровеньПодготовки: str
    ФормаОбучения: str
    Итог: str
    Бюджет: str
    БюджетИН: str
    Договор: str
    ДоговорИН: str
    БюджетСубъект: str
    БюджетСубъектИн: str
    МестныйБюджет: str
    МестныйБюджетИн: str
    Время: str
    Дата: str


class EducationFive(BaseModel): #  www.dipacademy.ru/sveden/education/obr-5/ Информация о результатах перевода, восстановления и отчисления
    Код: str
    Специальность: str
    УровеньПодготовки: str
    ФормаОбучения: str
    ПереводВ: str
    ПереводИЗ: str
    Востановленный: str
    Отчисленный: str
    Время: str
    Дата: str


logging.basicConfig(filename='load_education.log', filemode='a', format = '%(asctime)s  %(message)s')

def get_data_from_api(url, user=API_USER, password=API_PASSWORD):
    try:
        user = user.encode('utf-8')
        response_API = requests.get(url, auth=HTTPBasicAuth(user, password))
        if response_API.status_code == 404:
            logging.error('404 Page Not Found Error')
            raise SystemExit()
        elif response_API.status_code == 501:
            logging.error('501 Internal Server Error')
            raise SystemExit()
        else:
            data = response_API.text
            data = json.loads(data)
            return data
    except requests.exceptions.RequestException as exception:
        logging.error(f"RequestException {exception}")
        raise SystemExit(exception)

def get_data_from_json(file_path):
    try:
        with codecs.open(file_path, 'r', encoding='utf_8_sig') as file:
            data = json.load(file)
        return data
    except JSONDecodeError as exception:
        print(exception)


def get_data(api_url=False, file_path=False):
    try:
        if api_url:
            data = get_data_from_api(api_url)
            return data
        elif file_path:
            data = get_data_from_json(file_path)
            return data
        else:
            logging.error('Wrong path to file')
            raise SystemExit()
    except Exception as exception:
        logging.error(f"RequestException {exception}")
        raise SystemExit(exception)

def get_parsed_data_three(data):
    try:
        data_list = []
        for template in data:
            students_info= EducationThree(**template)
            data_row = (students_info.Код, # eduCode
                        students_info.Специальность, # eduName
                        students_info.УровеньПодготовки, # eduLevel
                        students_info.ФормаОбучения, # eduForm
                        students_info.Бюджет, # numberBF
                        students_info.БюджетИН, # numberBFF
                        students_info.БюджетСубъект, # numberBR,
                        students_info.БюджетСубъектИн, # numberBRF,
                        students_info.МестныйБюджет, # numberBM,
                        students_info.МестныйБюджетИн, # numberBMF,
                        students_info.Договор, #numberP
                        students_info.ДоговорИН,  #numberPF
                        students_info.Итог,  # numberAll
                        students_info.Время,
                        students_info.Дата
                        )
            data_list.append(str(data_row))
        return data_list
    except (ValidationError, JSONDecodeError) as exception:
        logging.error(f"Exception {exception}")
        raise SystemExit(exception)

def get_parsed_data_five(data):
    try:
        data_list = []
        for template in data:
            students_info= EducationFive(**template)
            data_row = (students_info.Код, # eduCode
                        students_info.Специальность, # eduName
                        students_info.УровеньПодготовки, # eduLevel
                        students_info.ФормаОбучения, #edu_form
                        students_info.ПереводВ, # number_out_perevod
                        students_info.ПереводИЗ, # number_to_perevod
                        students_info.Востановленный, # number_res_perevod
                        students_info.Отчисленный, # number_exp_perevod
                        students_info.Время,
                        students_info.Дата
                        )
            data_list.append(str(data_row))
        return data_list
    except (ValidationError, JSONDecodeError) as exception:
        logging.error(f"Exception {exception}")
        raise SystemExit(exception)

def database_connection(base_name=BASE_NAME, login=LOGIN, password=PASSWORD, host=HOST):
    try:
        connection = psycopg2.connect(dbname=base_name, user=login, password=password, host=host)
        return connection
    except (Exception, Error) as error:
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

def load_education_three_table():
    try:
        connection = database_connection()
        data = get_data(api_url=CHISLENNOST_API_URL)
        parsed_data = get_parsed_data_three(data)
        insert_data_to_table(connection, parsed_data, EDUCATION_THREE_TABLE, EDUCATION_THREE_FIELDS)
    except Exception as exception:
        logging.error(f"load_education_three_table exception {exception}")
        raise SystemExit(exception)

def load_education_five_table():
    try:
        connection = database_connection()
        data = get_data(api_url=CHISLENNOST_VOST_I_OT_API_URL)
        parsed_data = get_parsed_data_five(data)
        insert_data_to_table(connection, parsed_data, EDUCATION_FIVE_TABLE, EDUCATION_FIVE_FIELDS)
    except Exception as exception:
        logging.error(f"load_education_five_table exception {exception}")
        raise SystemExit(exception)

if __name__ == "__main__":
    # Численность
    load_education_three_table()

    # Информация о результатах перевода, восстановления и отчисления
    load_education_five_table()


    sys.exit()

