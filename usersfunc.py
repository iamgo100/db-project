'''
    Функции для работы с пользователем
    1. Работа с таблицей "соискатель (пользователь)":
        - добавление нового пользователя
        - изменение данных пользователя
    2. Работа с таблицей "резюме":
        - добавление нового резюме
        - изменение данных резюме
        - удаление резюме
    3. Работа с таблицей "компании":
        - добавление новой компании
        - изменение данных компании
    4. Работа с таблицей "вакансии":
        - добавление новой вакансии
        - изменение данных вакансии
        - удаление вакансии
    5. Работа с таблицей "филиалы":
        - добавление нового филиала
        - изменение данных филиала
        - удаление филиала
    6. Поиск по таблице "резюме" для представителей компаний
    7. Поиск по таблице "вакансии" для соискателей
'''
import basefunc as bf # Подключение базовых функций
import helpfunc as hf # Подключение вспомогательных функций

def add_user(conn, cur, login, password):
    values = []
    hf.alert('add')
    values.append(hf.cycle('Имя*: '))
    values.append(hf.cycle('Фамилия*: '))
    values.append(hf.cycle('Номер телефона*: '))
    hf.if_empty('Город: ',values)
    hf.if_empty('Статус (студент/выпускник): ',values)
    values.insert(0, login)
    values.insert(1, password)
    bf.add(conn, cur, 'users', values)

def change_user(conn, cur, login):
    columns = []; values = []
    hf.alert('change')
    hf.add_values_to_arrays('Логин: ', 'login', columns, values)
    hf.add_values_to_arrays('Пароль: ', 'password', columns, values)
    hf.add_values_to_arrays('Имя: ', 'fname', columns, values)
    hf.add_values_to_arrays('Фамилия: ', 'lname', columns, values)
    hf.add_values_to_arrays('Номер телефона: ', 'phone', columns, values)
    hf.add_values_to_arrays('Город: ', 'city', columns, values)
    hf.add_values_to_arrays('Статус (студент/выпускник): ', 'status', columns, values)
    bf.change(conn, cur, 'users', 'login', login, columns, values)
    if 'login' in columns:
        login = values[0]
    return login

def add_resume(conn, cur, login):
    values = []
    hf.alert('add')
    values.append(hf.cycle('Профессия*: '))
    hf.if_empty('Опыт работы в данной профессии: ', values)
    hf.if_empty('Занятость (полная/частичная): ', values)
    hf.if_empty('Вам нужна практика для вуза?\n(да/нет)\n', values)
    id_ = hf.search_id(conn, cur, 'resumes')
    values.insert(0, id_)
    values.insert(1, login)
    bf.add(conn, cur, 'resumes', values)
        
def change_resume(conn, cur):
    prKey = input('Введите ID резюме, которое хотите изменить: ')
    if not bf.search(conn, cur, 'resumes', ['id'], [prKey]):
        print('Резюме с таким ID не существует\n')
    else:
        columns = [];  values = []
        hf.alert('change')
        hf.add_values_to_arrays('Профессия: ', 'profession', columns, values)
        hf.add_values_to_arrays('Опыт работы в данной профессии: ', 'experience', columns, values)
        hf.add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns, values)
        hf.add_values_to_arrays('Вам важна практика для вуза? (да/нет)\n', 'practice', columns, values)
        bf.change(conn, cur, 'resumes', 'id', prKey, columns, values)

def delete_resume(conn, cur):
    prKey = input('Введите ID резюме, которое хотите удалить: ')
    if not bf.search(conn, cur, 'resumes', ['id'], [prKey]):
        print('Резюме с таким ID не существует\n')
    else:
        bf.delete(conn, cur, 'resumes', 'id', prKey)

def add_company(conn, cur, login, password):
    values = []
    hf.alert('add')
    values.append(hf.cycle('Сайт*: '))
    values.append(hf.cycle('Электронная почта компании (для связи)*: '))
    values.append(hf.cycle('Предусмотрена ли практика для студентов?* (да/нет)\n'))
    values.insert(0, login)
    values.insert(1, password)
    bf.add(conn, cur, 'companies', values)

def change_company(conn, cur, name):
    columns = [];  values = []
    hf.alert('change')
    hf.add_values_to_arrays('Название: ', 'login', columns, values)
    hf.add_values_to_arrays('Пароль: ', 'password', columns, values)
    hf.add_values_to_arrays('Сайт: ', 'site', columns, values)
    hf.add_values_to_arrays('Электронная почта компании (для связи): ', 'email', columns, values)
    hf.add_values_to_arrays('Предусмотрена ли практика для студентов? (да/нет)\n', 'practice', columns, values)
    bf.change(conn, cur, 'companies', 'login', name, columns, values)
    if 'login' in columns:
        name = values[0]
    return name

def add_vacancy(conn, cur):
    values = []
    hf.alert('add')
    values.append(hf.cycle('Вакансия (профессия)*: '))
    values.append(hf.cycle('ID филиала*: '))
    hf.if_empty('Занятость (полная/частичная): ', values)
    hf.if_empty('Зарплата: ', values)
    hf.if_empty('Опыт работы: ', values)
    id_ = hf.search_id(conn, cur, 'vacancies')
    values.insert(0, id_)
    bf.add(conn, cur, 'vacancies', values)

def change_vacancy(conn, cur):
    prKey = input('Введите ID вакансии, которую хотите изменить: ')
    if not bf.search(conn, cur, 'vacancies', ['id'], [prKey]):
        print('Вакансии с таким ID не существует')
    else:
        columns = [];  values = []
        hf.alert('change')
        hf.add_values_to_arrays('Вакансия (профессия): ', 'name', columns, values)
        hf.add_values_to_arrays('ID филиала: ', 'idOfFil', columns, values)
        hf.add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns, values)
        hf.add_values_to_arrays('Зарплата: ', 'pay', columns, values)
        hf.add_values_to_arrays('Опыт работы: ', 'experience', columns, values)
        bf.change(conn, cur, 'vacancies', 'id', prKey, columns, values)

def delete_vacancy(conn, cur):
    prKey = input('Введите ID вакансии, которую хотите удалить: ')
    if not bf.search(conn, cur, 'vacancies', ['id'], [prKey]):
        print('Вакансии с таким ID не существует')
    else:
        bf.delete(conn, cur, 'vacancies', 'id', prKey)

def add_fil(conn, cur, name):
    values = []
    hf.alert('add')
    values.append(hf.cycle('ID филиала*: '))
    values.append(hf.cycle('Город*: '))
    values.insert(1, name)
    bf.add(conn, cur, 'filiations', values)

def change_fil(conn, cur):
    prKey = input('Введите ID филиала, который хотите изменить: ')
    if not bf.search(conn, cur, 'filiations', ['id'], [prKey]):
        print('Филиала с таким ID не существует\n')
    else:
        columns = [];  values = []
        hf.alert('change')
        hf.add_values_to_arrays('ID филиала: ', 'id' , columns, values)
        hf.add_values_to_arrays('Город: ', 'city', columns, values)
        bf.change(conn, cur, 'filiations', 'id', prKey, columns, values)

def delete_fil(conn, cur):
    prKey = input('Введите ID филиала, который хотите удалить: ')
    if not bf.search(conn, cur, 'filiations', ['id'], [prKey]):
        print('Филиала с таким ID не существует\n')
    else:
        bf.delete(conn, cur, 'filiations', 'id', prKey)

def search_resume(conn, cur):
    hf.alert('search')
    columns_r = [];  values_r = []
    columns_u = [];  values_u = []
    hf.add_values_to_arrays('Профессия: ', 'profession', columns_r, values_r)
    hf.add_values_to_arrays('Опыт работы: ', 'experience', columns_r, values_r)
    hf.add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns_r, values_r)
    hf.add_values_to_arrays('Важна ли возможность практики? (да/нет)\n', 'practice', columns_r, values_r)
    hf.add_values_to_arrays('Город: ', 'city', columns_u, values_u)
    hf.add_values_to_arrays('Статус (студент/выпускник): ', 'status', columns_u, values_u)
    hf.making_res_entries(conn, cur, columns_u, values_u, columns_r, values_r)

def search_by_vacancy(conn, cur, name, header):
    columns_r = ['profession', 'experience', 'employment', 'practice']
    columns_u = ['city']
    company = bf.search(conn, cur, 'companies', ['login'], [name])
    pract = company[0][-1]
    fils = bf.search(conn, cur, 'filiations', ['nameOfComp'], [name])
    vacancies = hf.search_vacs_of_comp(conn, cur, name)
    if len(vacancies) == 1:
        for fil in fils:
            if fil[0] == vacancies[0][2]:
                city = fil[2]
                break
        values_r = [vacancies[0][1], vacancies[0][-1], vacancies[0][3], pract]
        values_u = [city]
        hf.making_res_entries(conn, cur, columns_u, values_u, columns_r, values_r)
    elif len(vacancies) > 1:
        hf.render(vacancies, header)
        id_ = int(input('Введите ID вакансии, по которой хотите искать резюме: '))
        print('')
        for vac in vacancies:
            if vac[0] == id_:
                for fil in fils:
                    if fil[0] == vac[2]:
                        city = fil[2]
                        break
                values_r = [vac[1], vac[-1], vac[3], pract]
                values_u = [city]
                hf.making_res_entries(conn, cur, columns_u, values_u, columns_r, values_r)
                break
    else:
        print('По вашему запросу ничего не найдено\n')

def search_vacancy(conn, cur):
    hf.alert('search')
    columns_v = [];  values_v = []
    columns_c = [];  values_c = []
    columns_cm = [];  values_cm = []
    hf.add_values_to_arrays('Вакансия (профессия): ', 'name', columns_v, values_v)
    hf.add_values_to_arrays('Занятость (полная/частичная): ', 'employment', columns_v, values_v)
    hf.add_values_to_arrays('Зарплата: ', 'pay', columns_v, values_v)
    hf.add_values_to_arrays('Опыт работы: ', 'experience', columns_v, values_v)
    hf.add_values_to_arrays('Город: ', 'city', columns_c, values_c)
    hf.add_values_to_arrays('Важна ли возможность практики? (да/нет)\n', 'practice', columns_cm, values_cm)
    hf.making_vac_entries(conn, cur, columns_v, values_v, columns_c, values_c, columns_cm, values_cm)

def search_by_resume(conn, cur, login, header):
    resumes = bf.search(conn, cur, 'resumes', ['login'], [login])
    user = bf.search(conn, cur, 'users', ['login'], [login])
    columns_v = ['name', 'experience', 'employment' ]
    columns_c = ['city']
    columns_cm = ['practice']
    if len(resumes) == 1:
        values_v = [resumes[0][2], resumes[0][3], resumes[0][4]]
        values_c = [user[0][5]]
        values_cm = [resumes[0][-1]]
        hf.making_vac_entries(conn, cur, columns_v, values_v, columns_c, values_c, columns_cm, values_cm)
    elif len(resumes) > 1:
        hf.render(resumes, header)
        id_ = int(input('Введите ID резюме, по которому хотите искать вакансии: '))
        print('')
        for res in resumes:
            if res[0] == id_:
                values_v = [res[2], res[3], res[4]]
                values_c = [user[0][5]]
                values_cm = [res[-1]]
                hf.making_vac_entries(conn, cur, columns_v, values_v, columns_c, values_c, columns_cm, values_cm)
                break
    else:
        print('По вашему запросу ничего не найдено\n')

if __name__ == '__main__':
    pass