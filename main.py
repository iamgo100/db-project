import sqlite3
import basefunc as bf #Подключение базовых функций
import usersfunc as uf #Подключение пользовательских функций

class companies:
    name = 'companies'
class users:
    name = 'users'
class filiations:
    name = 'filiations'
    header = '| ID филиала | Название компании | Город |'
class vacancies:
    name = 'vacancies'
    header = '''|    ID    |  Вакансия   |   ID    | Занятость | Зарплата | Опыт работы |
| вакансии | (профессия) | филиала |           |          |             |'''
class resumes:
    name = 'resumes'
    header = '| ID резюме | Логин соискателя | Профессия | Опыт работы | Занятость | Нужна ли практика |'

def render(entries, header):
    if not entries:
        print('По вашему запросу ничего не найдено\n')
    else:
        print(header)
        for entry in entries:
            print(entry)
        print('')
        
def search_id(conn, cur, table):
    res = bf.search(conn, cur, table, [], [])
    return len(res) + 1

def create_tables(conn):
    try:
        conn.execute('PRAGMA foreign_keys = on')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS companies
                        (login VARCHAR PRIMARY KEY,
                        password CHAR(8) NOT NULL,
                        site VARCHAR NOT NULL,
                        email VARCHAR NOT NULL,
                        practice VARCHAR NOT NULL)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS filiations
                        (id INTEGER PRIMARY KEY,
                        nameOfComp VARCHAR NOT NULL,
                        city VARCHAR NOT NULL,
                        FOREIGN KEY (nameOfComp) REFERENCES companies(login) ON UPDATE CASCADE ON DELETE CASCADE)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS vacancies
                        (id INTEGER PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        idOfFil INTEGER NOT NULL,
                        employment VARCHAR,
                        pay INTEGER,
                        experience VARCHAR,
                        FOREIGN KEY (idOfFil) REFERENCES filiations(id) ON UPDATE CASCADE ON DELETE CASCADE)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                        (login VARCHAR PRIMARY KEY,
                        password CHAR(8) NOT NULL,
                        fname VARCHAR NOT NULL,
                        lname VARCHAR NOT NULL,
                        phone CHAR(11) NOT NULL,
                        city VARCHAR,
                        status VARCHAR)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS resumes
                        (id INTEGER PRIMARY KEY,
                        login VARCHAR NOT NULL,
                        profession VARCHAR NOT NULL,
                        experience VARCHAR,
                        employment VARCHAR,
                        practice VARCHAR,
                        FOREIGN KEY (login) REFERENCES users(login) ON UPDATE CASCADE ON DELETE CASCADE)''')
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f'Ошибка создания таблиц: {e}')
        return False

def edit_fil(conn, cur, name):
    print('Выберите действие:')
    print('1. Добавить новый филиал в реестр')
    print('2. Изменить данные имеющегося филиала')
    print('3. Удалить филиал из реестра')
    print('4. Вернуться в главное меню')
    
    while True:
        num = input('Введите пункт меню: ')
        print('')
        if num == '1':
            values = uf.add_fil()
            values.insert(1, name)
            bf.add(conn, cur, 'filiations', values)
            edit_fil(conn, cur, name)
            break
        elif num == '2':
            prKey = input('Введите ID филиала, который хотите изменить: ')
            if not bf.search(conn, cur, 'filiations', ['id'], [prKey]):
                print('Филиала с таким ID не существует\n')
            else:
                columns, values = uf.enter_fil()
                bf.change(conn, cur, 'filiations', 'id', prKey, columns, values)
            edit_fil(conn, cur, name)
            break
        elif num == '3':
            prKey = input('Введите ID филиала, который хотите удалить: ')
            if not bf.search(conn, cur, 'filiations', ['id'], [prKey]):
                print('Филиала с таким ID не существует\n')
            else:
                bf.delete(conn, cur, 'filiations', 'id', prKey)
            edit_fil(conn, cur, name)
            break
        elif num == '4':
            menu_for_comp(conn, cur, name)
            break
        else:
            print('Такого пункта в меню нет.\n')
    
def edit_vac(conn, cur, name):
    print('Выберите действие:')
    print('1. Добавить новую вакансию в реестр')
    print('2. Изменить данные имеющейся вакансии')
    print('3. Удалить вакансию из реестра')
    print('4. Вернуться в главное меню')
    
    while True:
        num = input('Введите пункт меню: ')
        print('')
        if num == '1':
            values = uf.add_vacancy()
            id_ = search_id(conn, cur, 'vacancies')
            values.insert(0, id_)
            bf.add(conn, cur, 'vacancies', values)
            edit_vac(conn, cur, name)
            break
        elif num == '2':
            prKey = input('Введите ID вакансии, которую хотите изменить: ')
            if not bf.search(conn, cur, 'vacancies', ['id'], [prKey]):
                print('Вакансии с таким ID не существует')
            else:
                columns, values = uf.enter_vacancy()
                bf.change(conn, cur, 'vacancies', 'id', prKey, columns, values)
            edit_vac(conn, cur, name)
            break
        elif num == '3':
            prKey = input('Введите ID вакансии, которую хотите удалить: ')
            if not bf.search(conn, cur, 'vacancies', ['id'], [prKey]):
                print('Вакансии с таким ID не существует')
            else:
                bf.delete(conn, cur, 'vacancies', 'id', prKey)
            edit_vac(conn, cur, name)
            break
        elif num == '4':
            menu_for_comp(conn, cur, name)
            break
        else:
            print('Такого пункта в меню нет.\n')

def menu_for_comp(conn, cur, name):
    print('ГЛАВНОЕ МЕНЮ\n')
    print('1. Поиск резюме')
    print('2. Изменение данных компании')
    print('3. Удалить аккаунт компании')
    print('4. Посмотреть имеющиеся филиалы')
    print('5. Посмотреть имеющиеся вакансии')
    print('6. Выход')
    
    while True:
        num = input('Выберите пункт меню: ')
        print('')
        if num == '1':
            res = uf.search_resume(conn, cur)
            header = '''|   ID   | Имя | Фамилия |   Номер  | Город | Статус | Профессия |  Опыт  | Занятость | Нужна ли |
| резюме |     |         | телефона |       |        |           | работы |           | практика |'''
            render(res, header)
            answer = input('Вернутся в главное меню? (да/нет)\n')
            print('')
            if answer == 'нет':
                print('До свидания!')
            else:
                menu_for_comp(conn, cur, name)
            break
        elif num == '2':
            columns, values = uf.enter_company()
            bf.change(conn, cur, 'companies', 'login', name, columns, values)
            if 'login' in columns:
                name = values[0]
            menu_for_comp(conn, cur, name)
            break
        elif num == '3':
            answer = input('Вы уверены, что хотите удалить аккаунт компании, а также все вакансии и филиалы, связанные с ней? (да/нет)\n')
            if answer == 'да':
                bf.delete(conn, cur, 'companies', 'login', name)
                print('До свидания!')
            else:
                menu_for_comp(conn, cur, name)
            break
        elif num == '4':
            res = bf.search(conn, cur, 'filiations', ['nameOfComp'], [name])
            render(res, filiations.header)
            answer = input('Хотите редактировать данные филиалов? (да/нет)\n')
            print('')
            if answer == 'да':
                edit_fil(conn, cur, name)
            else:
                menu_for_comp(conn, cur, name)
            break
        elif num == '5':
            values = bf.search(conn, cur, 'filiations', ['nameOfComp'], [name])
            if values:
                columns = []
                newValues = []
                for val in values:
                    columns.append('idOfFil')
                    newValues.append(val[0])
                res = bf.search(conn, cur, 'vacancies', columns, newValues)
                render(res, vacancies.header)
                answer = input('Хотите редактировать данные вакансий? (да/нет)\n')
                print('')
                if answer == 'да':
                    edit_vac(conn, cur, name)
            else:
                print('У вас пока нет ни одного филиала, чтобы редактировать вакансии.')
                answer = input('Хотите редактировать данные филиалов? (да/нет)\n')
                print('')
                if answer == 'да':
                    edit_fil(conn, cur, name)
            menu_for_comp(conn, cur, name)            
            break
        elif num == '6':
            print('До свидания!')
            break
        else:
            print('Такого пункта в меню нет\n')

def view_resume(conn, cur, login):
    res = bf.search(conn, cur, 'resumes', ['login'], [login])
    render(res, resumes.header)
    while True:
        print('Выберите дальнешее действие:')
        print('1. Изменить имеющееся резюме')
        print('2. Удалить имеющееся резюме')
        print('3. Вернутся в главное меню')
        num = input('Введите пункт меню: ')
        print('')
        if num == '1':
            prKey = input('Введите ID резюме, которое хотите изменить: ')
            if not bf.search(conn, cur, 'resumes', ['id'], [prKey]):
                print('Резюме с таким ID не существует\n')
            else:
                columns, values = uf.enter_resume()
                bf.change(conn, cur, 'resumes', 'id', prKey, columns, values)
        elif num == '2':
            prKey = input('Введите ID резюме, которое хотите удалить: ')
            if not bf.search(conn, cur, 'resumes', ['id'], [prKey]):
                print('Резюме с таким ID не существует\n')
            else:
                bf.delete(conn, cur, 'resumes', 'id', prKey)
        elif num == '3':
            menu_for_st(conn, cur, login)
            break
        else:
            print('Такого пункта в меню нет.\n')

def menu_for_st(conn, cur, login):
    print('ГЛАВНОЕ МЕНЮ\n')
    print('1. Поиск вакансий')
    print('2. Изменить аккаунт')
    print('3. Удалить аккаунт')
    print('4. Добавить новое резюме')
    print('5. Посмотреть имеющиеся резюме')
    print('6. Выход')
    
    while True:
        num = input('Выберите пункт меню: ')
        print('')
        if num == '1':
            res = uf.search_vacancy(conn, cur)
            header = '''|    ID    | Профессия | Город | Занятость | Зарплата |  Опыт  | Название | Сайт | Электронная | Есть ли  |
| вакансии |           |       |           |          | работы | компании |      |    почта    | практика |'''
            render(res, header)
            answer = input('Вернутся в главное меню? (да/нет)\n')
            print('')
            if answer == 'нет':
                print('До свидания!')
            else:
                menu_for_st(conn, cur, login)
            break
        elif num == '2':
            columns, values = uf.enter_user()
            bf.change(conn, cur, 'users', 'login', login, columns, values)
            if 'login' in columns:
                login = values[0]
            menu_for_st(conn, cur, login)
            break
        elif num == '3':
            answer = input('Вы уверены, что хотите удалить свой аккаунт? (да/нет)\n')
            if answer == 'да':
                bf.delete(conn, cur, 'users', 'login', login)
                print('До свидания!')
            else:
                menu_for_st(conn, cur, login)
            break
        elif num == '4':
            values = uf.add_resume()
            id_ = search_id(conn, cur, 'resumes')
            values.insert(0, id_)
            values.insert(1, login)
            bf.add(conn, cur, 'resumes', values)
            menu_for_st(conn, cur, login)
            break
        elif num == '5':
            view_resume(conn, cur, login)
            break
        elif num == '6':
            print('До свидания!')
            break
        else:
            print('Такого пункта в меню нет.\n')

def authorization(conn, cur, table):
    while True:
        print('Введите данные')
        login = input('Логин: ')
        password = input('Пароль: ')
        if not login or not password:
            print('Неверный ввод логина или пароля')
        else:
            if not bf.search(conn, cur, table.name, ['login', 'password'], [login, password]):
                print('Неверный ввод логина или пароля')
            else:
                return login

def enter(conn, cur, table):
    print('1. Авторизация')
    print('2. Регистрация')
    print('3. Выход')
    while True:
        num = input('Выберите пункт меню: ')
        print('')
        if num == '1':
            login = authorization(conn, cur, table)
            if table.name == 'companies':
                menu_for_comp(conn, cur, login)
            else:
                menu_for_st(conn, cur, login)
            break
        elif num == '2':
            if table.name == 'companies':
                while True:
                    login = input('Введите название компании (далее оно будет использоваться как ваш логин для входа в систему): ')
                    if not bf.search(conn, cur, 'companies', ['login'], [login]):
                        while True:
                            password = input('Придумайте восьмизначный пароль: ')
                            if len(password) == 8:
                                values = uf.add_company()
                                values.insert(0, login)
                                values.insert(1, password)
                                bf.add(conn, cur, 'companies', values)
                                menu_for_comp(conn, cur, login)
                                break
                            else:
                                print('В пароле должно быть 8 символов!')
                        break
                    else:
                        print('Компания с таким названием уже существует.')
            else:
                while True:
                    login = input('Придумайте логин: ')
                    if not bf.search(conn, cur, 'users', ['login'], [login]):
                        while True:
                            password = input('Придумайте восьмизначный пароль: ')
                            if len(password) == 8:
                                values = uf.add_user()
                                values.insert(0, login)
                                values.insert(1, password)
                                bf.add(conn, cur, 'users', values)
                                menu_for_st(conn, cur, login)
                                break
                            else:
                                print('В пароле должно быть 8 символов!')
                        break
                    else:
                        print('Пользователь с таким логином уже существует.')
            break
        elif num == '3':
            print('До свидания!')
            break
        else:
            print('Такого пункта в меню нет.\n')

def main_menu(conn, cur):
    while True:
        print('Представьтесь, пожалуйста:')
        print('1. Я - представитель компании.')
        print('2. Я - студент/выпускник ВУЗа.\n')
        print('3. Выход.\n')
        num = input('Выберите пункт меню: ')
        print('\n')
        if num == '1':
            enter(conn, cur, companies)
            break
        elif num == '2':
            enter(conn, cur, users)
            break
        elif num == '3':
            print('До свидания!')
            break
        else:
            print('Такого пункта в меню нет.\n')

def main():
    try:
        conn = sqlite3.connect('example.db')
    except sqlite3.Error:
        print('Ошибка соединения с базой данных')
    else:
        cur = conn.cursor()
        conn.commit()
    
        if create_tables(conn):
            print('Добро пожаловать!\n')
            main_menu(conn, cur)
    
    conn.close()

main()