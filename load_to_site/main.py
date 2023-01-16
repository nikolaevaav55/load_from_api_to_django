import sys

from db_fields import *
from get_data import *
from db_insert import *


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

PREPODAVATELI_API_URL = os.getenv('PREPODAVATELI_API_URL')
CHISLENNOST_API_URL = os.getenv('CHISLENNOST_API_URL')
CHISLENNOST_VOST_I_OT_API_URL = os.getenv('CHISLENNOST_VOST_I_OT_API_URL')

logging.basicConfig(filename='main.py.log', filemode='a', format = '%(asctime)s  %(message)s')


if __name__ == "__main__":
    try:
        connection = database_connection()
        data_teacher = get_data(api_url=PREPODAVATELI_API_URL)
        parsed_data_teachers = get_parsed_teachers_data(data_teacher)
        insert_data_to_table(connection, parsed_data_teachers, TEACHERS, TEACHERS_MODELS_FIELDS)
    except Exception as exception:
        logging.error(f"Teachers load EXCEPTION : {exception}")

    try:
        connection = database_connection()
        data_students_three = get_data(api_url=CHISLENNOST_API_URL)
        parsed_data_students_three = get_parsed_data_three(data_students_three)
        insert_data_to_table(connection, parsed_data_students_three, EDUCATION_THREE_TABLE, EDUCATION_THREE_FIELDS)
    except Exception as exception:
        logging.error(f"Students_three load EXCEPTION : {exception}")

    try:
        connection = database_connection()
        data_students_five = get_data(api_url=CHISLENNOST_VOST_I_OT_API_URL)
        parsed_data_students_five = get_parsed_data_five(data_students_five)
        insert_data_to_table(connection, parsed_data_students_five, EDUCATION_FIVE_TABLE, EDUCATION_FIVE_FIELDS)
    except Exception as exception:
        logging.error(f"Students_three load EXCEPTION : {exception}")

    sys.exit()