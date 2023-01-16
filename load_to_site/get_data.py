import os
from dotenv import load_dotenv
import requests
import logging
import json
import codecs
import pydantic

from requests.auth import HTTPBasicAuth

from validation_models import Teachers, EducationThree, EducationFive

logging.basicConfig(filename='load_to_site.log', filemode='a', format = '%(asctime)s  %(message)s')

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')


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
    except json.JSONDecodeError as exception:
        logging.error(f"JSONDecodeError {exception}")

def get_data(api_url=False, file_path=False):
    try:
        if api_url:
            data = get_data_from_api(api_url)
            return data
        elif file_path:
            data = get_data_from_json(file_path)
            return data
        else:
            logging.error(f'Wrong path to file: {api_url, file_path}')
            raise SystemExit()
    except Exception as exception:
        logging.error(f"get_data_Exception {exception}")
        raise SystemExit(exception)

def get_parsed_teachers_data(data):
    try:
        data_list = []
        for template in data:
            teachers= Teachers(**template)
            programms_str = ''
            if teachers.УчебныйПроцесс:
                programms = set([programm.ОбразовательнаяПрограмма for programm in teachers.УчебныйПроцесс])
                programms_str = str(programms)
            data_row = (teachers.Должность,
                        teachers.УченыеСтепени.replace('\\n','<br>'),
                        teachers.УченоеЗвание,
                        teachers.УровеньОбразования,
                        teachers.ОбщийСтаж,
                        teachers.СтажПоСпециальности,
                        teachers.ПреподаваемыеДисциплины.replace('\\n',', '),
                        teachers.Квалификации.capitalize().replace('\\n',', '),
                        teachers.НаправленияПодготовкиИСпециальности.replace('\\n',', '),
                        teachers.ФизическоеЛицо,
                        teachers.СписокПовышенийКвалификаций.replace('\\n','<br><br>').replace("'", ""), #replace нужен, чтобы измежать проблем с апострафом
                        teachers.Звания.replace(",", ""),
                        teachers.Кафедра.strip(),
                        teachers.Направление,
                        teachers.Фотография,
                        teachers.Код,
                        teachers.ДополнительнаяИнформация1.replace('\n\n','<br><br>').replace('\n','<br>'),
                        teachers.ДополнительнаяИнформация2.replace('\n\n','<br><br>').replace('\n','<br>'),
                        teachers.Публикации.replace('\n\n','<br><br>').replace('\n','<br>'),
                        teachers.СфераНаучныхИнтересов.replace('\n\n','<br><br>').replace('\n','<br>'),
                        teachers.ЯвляетсяАвтором.replace('\n\n','<br><br>').replace('\n','<br>'),
                        teachers.ДатаРождения,
                        teachers.Телефон,
                        teachers.Емайл,
                        teachers.Сайт,
                        teachers.УИД,
                        programms_str.replace('{','').replace(',', '<br>').replace("'", '').replace('}', '')
                        )
            data_list.append(str(data_row))
        return data_list
    except (pydantic.ValidationError, json.JSONDecodeError) as exception:
        logging.error(f"Exception {exception}")
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
    except (pydantic.ValidationError, json.JSONDecodeError) as exception:
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
    except (pydantic.ValidationError, json.JSONDecodeError) as exception:
        logging.error(f"Exception {exception}")
        raise SystemExit(exception)