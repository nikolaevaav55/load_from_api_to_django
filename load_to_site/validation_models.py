from pydantic import BaseModel
from typing import List, Optional


class StudyingProccess(BaseModel):
    КодСпециальности: Optional[str] = None
    НаименованиеСпецальности: Optional[str] = None
    ОбразовательнаяПрограмма: Optional[str] = None
    Дисциплина: Optional[str] = None

class Teachers(BaseModel):
    Должность: str
    УченыеСтепени: str
    УченоеЗвание: str
    УровеньОбразования: str
    ОбщийСтаж: str
    СтажПоСпециальности: str
    ПреподаваемыеДисциплины: str
    Квалификации: str
    НаправленияПодготовкиИСпециальности: str
    ФизическоеЛицо: str
    СписокПовышенийКвалификаций: str
    Звания: str
    Кафедра: str
    Направление: str
    Фотография: str
    Код: str
    СфераНаучныхИнтересов: str
    Публикации: str
    ЯвляетсяАвтором: str
    ДополнительнаяИнформация1: str
    ДополнительнаяИнформация2: str
    ДатаРождения: str
    Телефон: str
    Емайл: str
    Сайт: str
    УченыеСтепени: str
    УИД: str
    УчебныйПроцесс: List[StudyingProccess]

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