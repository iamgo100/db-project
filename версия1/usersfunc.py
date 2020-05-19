'''
    Функции для работы с пользователем
    1. Работа с таблицей "резюме":
        - добавление нового резюме
        - выборка по таблице "резюме"
    2. Работа с таблицей "вакансии":
        - добавление новой вакансии
        - выборка по таблице "вакансии"
        - сложный поиск по таблице "вакансии"
    3. Работа с таблицей "компании":
        - добавление новой компании
        - выборка по таблице "компании"
    4. Работа с таблицей "филиалы":
        - добавление нового филиала
        - выборка по таблице "филиалы"
'''
import sqlite3
import re

def cycle(row):
    while True:
        param = input(row)
        if param == '':
            print('Поле является обязательным, введите данные.')
        else:
            return param

def add_values_to_arrays(prompt,column,columns,values):
    value = input(prompt)
    if value != '':
        arr = value.split(', ')
        for i in range(len(arr)):
            columns.append(column)
            values.append(arr[i])

def if_empty(prompt,values):
    value = input(prompt)
    if value == '':
        values.append('-')
    else:
        values.append(value)

def add_resume():
    values = []
    print('Введите данные для каждого столбца\nЕсли хотите пропустить ввод данных столбца, нажмите Enter')
    print('Обязательные поля помечены звездочкой *\n')
    values.append(cycle('ID резюме*: '))
    values.append(cycle('Имя*: '))
    values.append(cycle('Фамилия*: '))
    values.append(cycle('Номер телефона*: '))
    if_empty('Город: ',values)
    if_empty('Статус (студент/выпускник): ',values)
    if_empty('Профессия: ',values)
    if_empty('Опыт работы в данной профессии: ',values)
    if_empty('Занятость (полная/частичная): ',values)
    if_empty('Вам нужна практика для вуза?\n(да/нет)\n: ',values)
    return values
        
def enter_resume():
    columns = [];  values = []
    add_values_to_arrays('Имя: ','fname',columns,values)
    add_values_to_arrays('Фамилия: ','sname',columns,values)
    add_values_to_arrays('Номер телефона: ','phone',columns,values)
    add_values_to_arrays('Город: ','city',columns,values)
    status = input('Статус (студент/выпускник): ')
    if status != '':
        columns.append('status')
        values.append(status)
    profession = input('Профессия: ')
    if profession != '':
        columns.append('profession')
        values.append(profession)
    experience = input('Опыт работы в данной профессии: ')
    if experience != '':
        columns.append('experience')
        values.append(experience)
    employment = input('Занятость (полная/частичная): ')
    if employment != '':
        columns.append('employment')
        values.append(employment)
    practice = input('Вам важна практика для вуза?\n(да/нет)\n')
    if practice != '':
        columns.append('practice')
        values.append(practice)
    return [columns, values]

def add_vacancy():
    values = []
    print('Введите данные для каждого столбца\nЕсли хотите пропустить ввод данных столбца, нажмите Enter')
    print('Обязательные поля помечены звездочкой *\n')
    values.append(cycle('ID вакансии*: '))
    values.append(cycle('Вакансия (профессия)*: '))
    values.append(cycle('Название компании*: '))
    values.append(cycle('ID филиала*: '))
    if_empty('Занятость (полная/частичная): ',values)
    if_empty('Зарплата: ',values)
    if_empty('Опыт работы: ',values)
    return values

def enter_vacancy():
    columns = [];  values = []
    name = input('Вакансия (профессия): ')
    if name != '':
        columns.append('name')
        values.append(name)
    nameOfComp = input('Название компании: ')
    if nameOfComp != '':
        columns.append('nameOfComp')
        values.append(nameOfComp)
    idOfFil = input('ID филиала: ')
    if idOfFil != '':
        columns.append('idOfFil')
        values.append(idOfFil)
    employment = input('Занятость (полная/частичная): ')
    if employment != '':
        columns.append('employment')
        values.append(employment)
    pay = input('Зарплата: ')
    if pay != '':
        columns.append('pay')
        values.append(pay)
    experience = input('Опыт работы: ')
    if experience != '':
        columns.append('experience')
        values.append(experience)
    return [columns, values]

def search_vacancy(conn, cur):
    queryList = []
    name = input('Вакансия (профессия): ')
    if name != '':
        arr = name.split(', ')
        query = '('
        for i in range(len(arr)):
            query = query + f'name = "{arr[i]}"'
            if i != len(arr) - 1:
                query = query + ' OR '
            else:
                query = query + ' OR name = "-")'
        queryList.append(query)
    nameOfComp = input('Название компании: ')
    if nameOfComp != '':
        arr = name.split(', ')
        query = '('
        for i in range(len(arr)):
            query = query + f'nameOfComp = "{arr[i]}"'
            if i != len(arr) - 1:
                query = query + ' OR '
            else:
                query = query + ' OR nameOfComp = "-")'
        queryList.append(query)
    else:
        practice = input('Вам важна возможность пройти практику для вуза в компании?\n(да/нет)\n')
        if practice == 'да':
            queryn = 'SELECT name FROM companies WHERE practice = "да"'
            res = cur.execute(queryn).fetchall()
            conn.commit()
            if res != []:
                query = '('
                for i in range(len(res)):
                    query = query + f'nameOfComp = "{str(res[i][0])}"'
                    if i != len(res) - 1:
                        query = query + ' OR '
                    else:
                        query = query + ')'
                queryList.append(query)
    idOfFil = input('ID филиала или город: ')
    if idOfFil != '':
        arr = idOfFil.split(', ')
        query = '('
        if re.search('[0-9]',idOfFil) == None:
            queryn = 'SELECT id FROM filiations WHERE '
            for i in range(len(arr)):
                queryn = queryn + f'city = "{str(arr[i])}"'
                if i != len(arr) - 1:
                    queryn = queryn + ' OR '
            res = cur.execute(queryn).fetchall()
            conn.commit()
            if res != []:
                for i in range(len(res)):
                    query = query + f'idOfFil = "{str(res[i][0])}"'
                    if i != len(res) - 1:
                        query = query + ' OR '
                    else:
                        query = query + ')'
                queryList.append(query)
        else:
            for i in range(len(arr)):
                query = query + f'idOfFil = "{str(arr[i])}"'
                if i != len(arr) - 1:
                    query = query + ' OR '
                else:
                    query = query + ')'
            queryList.append(query)
    employment = input('Занятость (полная/частичная): ')
    if employment != '':
        queryList.append(f'(employment = "{employment}" OR employment = "-")')
    pay = input('Зарплата: ')
    if pay != '':
        queryList.append(f'(pay >= {pay} OR pay = "-")')
    experience = input('Опыт работы: ')
    if experience != '':
        queryList.append('f(experience = "{experience}" OR experience = "-")')
    if queryList != []:
        resultQuery = ' WHERE ' + ' AND '.join(queryList)
    else:
        resultQuery = ''
    return resultQuery

def add_company():
    values = []
    print('Введите данные для каждого столбца\nЕсли хотите пропустить ввод данных столбца, нажмите Enter')
    print('Обязательные поля помечены звездочкой *\n')
    values.append(cycle('Название*: '))
    values.append(cycle('Сайт*: '))
    values.append(cycle('Электронная почта компании (для связи)*: '))
    values.append(cycle('Предусмотрена ли практика для студентов?*\n(да/нет)\n'))
    return values

def enter_company():
    columns = [];  values = []
    add_values_to_arrays('Название: ','name',columns,values)
    site = input('Сайт: ')
    if site != '':
        columns.append('site')
        values.append(site)
    email = input('Электронная почта компании (для связи): ')
    if email != '':
        columns.append('email')
        values.append(email)
    practice = input('Предусмотрена ли практика для студентов?\n(да/нет)\n')
    if practice != '':
        columns.append('practice')
        values.append(practice)
    return [columns, values]

def add_fil():
    values = []
    print('Введите данные для каждого столбца\nЕсли хотите пропустить ввод данных столбца, нажмите Enter')
    print('Обязательные поля помечены звездочкой *\n')
    values.append(cycle('ID филиала*: '))
    values.append(cycle('Город*: '))
    return values

def enter_fil():
    columns = [];  values = []
    add_values_to_arrays('ID филиала: ','id',columns,values)
    add_values_to_arrays('Город: ','city',columns,values)
    return [columns, values]

if __name__ == '__main__':
    pass