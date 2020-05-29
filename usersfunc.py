'''
    alert - процерура оповещения пользователя, как вводить данные
    cycle - функция ввода обязательного параметра
    add_values_to_arrays - функция ввода параметров
    if_empty - функция проверки ввода на заполненность
    
    Функции для работы с пользователем
    1. Работа с таблицей "соискатель (пользователь)":
        - добавление нового пользователя
        - выборка по таблице
    2. Работа с таблицей "резюме":
        - добавление нового резюме
        - выборка по таблице
    3. Работа с таблицей "вакансии":
        - добавление новой вакансии
        - выборка по таблице
    4. Работа с таблицей "компании":
        - добавление новой компании
        - выборка по таблице
    5. Работа с таблицей "филиалы":
        - добавление нового филиала
        - выборка по таблице
    6. Поиск по таблице "резюме" для представителей компаний
    7. Поиск по таблице "вакансии" для соискателей
'''
import sqlite3
import re
import basefunc as bf

def alert(action):
    if action == 'add':
        print('Введите данные для каждого столбца')
        print('Если хотите пропустить ввод данных столбца, нажмите Enter')
        print('Обязательные поля помечены звездочкой *')
    elif action == 'enter':
        print('Введите новые данные для столбцов')
        print('Если не хотите изменять данные столбца, пропустите ввод, нажав Enter')
    elif action == 'search':
        print('Введите данные столбцов для поиска')
        print('Для введения нескольких параметров поиска для одного столбика,')
        print('разделяйте значения запятой и пробелом (", ")')
        print('Если хотите пропустить ввод данных столбца, нажмите Enter')
    print('\n')

def cycle(row):
    while True:
        param = input(row)
        if not param:
            print('Поле является обязательным, введите данные.')
        else:
            return param

def add_values_to_arrays(prompt, column, columns, values):
    value = input(prompt)
    if value:
        arr = value.split(', ')
        for value in arr:
            columns.append(column)
            values.append(value)

def if_empty(prompt, values):
    value = input(prompt)
    if not value:
        values.append('-')
    else:
        values.append(value)

def add_user():
    values = []
    alert('add')
    values.append(cycle('Имя*: '))
    values.append(cycle('Фамилия*: '))
    values.append(cycle('Номер телефона*: '))
    if_empty('Город: ',values)
    if_empty('Статус (студент/выпускник): ',values)
    return values

def enter_user():
    columns = []; values = []
    alert('enter')
    add_values_to_arrays('Логин: ', 'fname', columns, values)
    add_values_to_arrays('Пароль: ', 'fname', columns, values)
    add_values_to_arrays('Имя: ', 'fname', columns, values)
    add_values_to_arrays('Фамилия: ', 'sname', columns, values)
    add_values_to_arrays('Номер телефона: ', 'phone', columns, values)
    add_values_to_arrays('Город: ', 'city', columns, values)
    add_values_to_arrays('Статус (студент/выпускник): ', 'status', columns, values)
    return [columns, values]

def add_resume():
    values = []
    alert('add')
    values.append(cycle('Профессия*: '))
    if_empty('Опыт работы в данной профессии: ', values)
    if_empty('Занятость (полная/частичная): ', values)
    if_empty('Вам нужна практика для вуза?\n(да/нет)\n: ', values)
    return values
        
def enter_resume():
    columns = [];  values = []
    alert('enter')
    add_values_to_arrays('Профессия: ', 'profession', columns, values)
    add_values_to_arrays('Опыт работы в данной профессии: ', 'experience', columns, values)
    add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns, values)
    add_values_to_arrays('Вам важна практика для вуза? (да/нет)\n: ', 'practice', columns, values)
    return [columns, values]

def add_vacancy():
    values = []
    alert('add')
    values.append(cycle('Вакансия (профессия)*: '))
    values.append(cycle('ID филиала*: '))
    if_empty('Занятость (полная/частичная): ', values)
    if_empty('Зарплата: ', values)
    if_empty('Опыт работы: ', values)
    return values

def enter_vacancy():
    columns = [];  values = []
    alert('enter')
    add_values_to_arrays('Вакансия (профессия): ', 'name', columns, values)
    add_values_to_arrays('ID филиала: ', 'idOfFil', columns, values)
    add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns, values)
    add_values_to_arrays('Зарплата: ', 'pay', columns, values)
    add_values_to_arrays('Опыт работы: ', 'experience', columns, values)
    return [columns, values]

def add_company():
    values = []
    alert('add')
    values.append(cycle('Сайт*: '))
    values.append(cycle('Электронная почта компании (для связи)*: '))
    values.append(cycle('Предусмотрена ли практика для студентов?*\n(да/нет)\n'))
    return values

def enter_company():
    columns = [];  values = []
    alert('enter')
    add_values_to_arrays('Название: ', 'name', columns, values)
    add_values_to_arrays('Пароль: ', 'password', columns, values)
    add_values_to_arrays('Сайт: ', 'site', columns, values)
    add_values_to_arrays('Электронная почта компании (для связи): ', 'email', columns, values)
    add_values_to_arrays('Предусмотрена ли практика для студентов?\n(да/нет)\n', 'practice', columns, values)
    return [columns, values]

def add_fil():
    values = []
    alert('add')
    values.append(cycle('ID филиала*: '))
    values.append(cycle('Город*: '))
    return values

def enter_fil():
    columns = [];  values = []
    alert('enter')
    add_values_to_arrays('ID филиала: ', 'id' , columns, values)
    add_values_to_arrays('Город: ', 'city', columns, values)
    return [columns, values]

def search_resume(conn, cur):
    alert('search')
    columns_r = [];  values_r = []
    columns_u = [];  values_u = []
    entries = []
    add_values_to_arrays('Профессия: ', 'profession', columns_r, values_r)
    add_values_to_arrays('Опыт работы: ', 'experience', columns_r, values_r)
    add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns_r, values_r)
    add_values_to_arrays('Важна ли возможность практики? (да/нет)\n: ', 'practice', columns_r, values_r)
    add_values_to_arrays('Город: ', 'city', columns_u, values_u)
    add_values_to_arrays('Статус (студент/выпускник): ', 'status', columns_u, values_u)
    users = bf.search(conn, cur, 'users', [columns_u, values_u])
    if users:
        for user in users:
            columns_r.append('login')
            values_r.append(user[0])
    elif columns_r and values_r:
        resumes = bf.search(conn, cur, 'resumes', [columns_r, values_r])
        if resumes:
            for resume in resumes:
                user = bf.search(conn, cur, 'users', ['login', resume[1]])
                entry = (resume[0], user[2:], resume[2:])
                entries.append(entry)
    return entries

def search_vacancy(conn, cur):
    alert('search')
    columns_v = [];  values_v = []
    columns_c = [];  values_c = []
    columns_cm = [];  values_cm = []
    inf = []
    entries = []
    add_values_to_arrays('Вакансия (профессия): ', 'name', columns_v, values_v)
    add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns_v, values_v)
    add_values_to_arrays('Зарплата: ', 'pay', columns_v, values_v)
    add_values_to_arrays('Опыт работы: ', 'experience', columns_v, values_v)
    add_values_to_arrays('Город: ', 'city', columns_c, values_c)
    add_values_to_arrays('Важна ли возможность практики? (да/нет)\n: ', 'practice', columns_cm, values_cm)
    if columns_cm and values_cm:
        companies = bf.search(conn, cur, 'companies', [columns_cm, values_cm])
    elif columns_c and values_c:
        filiations = bf.search(conn, cur, 'filiations', [columns_c, values_c])
        if companies:
            for fil in filiations:
                for comp in companies:
                    if fil[1] == comp[0]:
                        columns_v.append('idOfFil')
                        values_v.append(fil[0])
                        inf.append((fil[0], fil[2], comp[4]))
                        break
    elif columns_v and values_v:
        vacancies = bf.search(conn, cur, 'vacancies', [columns_v, values_v])
        if vacancies:
            for vac in vacancies:
                for i in inf:
                    if vac[2] == i[0]:
                        entry = (vac[:1], i[1], vac[3:], i[2])
                        entries.append(entry)
                        break
    return entries

if __name__ == '__main__':
    pass