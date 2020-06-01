import sqlite3
import basefunc as bf # Подключение базовых функций
import usersfunc as uf # Подключение пользовательских функций
import helpfunc as hf # Подключение вспомогательных функций

class companies:
    name = 'companies'
class users:
    name = 'users'
class filiations:
    name = 'filiations'
    header = ['ID филиала', 'Название компании', '  Город  ']
class vacancies:
    name = 'vacancies'
    header = ['   ID   ', '   Вакансия    ', '  ID   ', 'Занятость', 'Зарплата', 'Опыт работы', '\n',
              'вакансии', '  (профессия)  ', 'филиала', '         ', '        ', '           ']
class resumes:
    name = 'resumes'
    header = ['ID резюме', 'Логин соискателя', '   Профессия   ', 'Опыт работы', 'Занятость', 'Нужна ли практика']

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

def view_fil(conn, cur, name):
    res = bf.search(conn, cur, 'filiations', ['nameOfComp'], [name])
    hf.render(res, filiations.header)
    answer = input('Хотите редактировать данные филиалов? (да/нет)\n')
    print('')
    if answer == 'да':
        return edit_fil(conn, cur, name)
    return menu_for_comp(conn, cur, name)

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
            uf.add_fil(conn, cur, name)
            return edit_fil(conn, cur, name)
        elif num == '2':
            uf.change_fil(conn, cur)
            return edit_fil(conn, cur, name)
        elif num == '3':
            uf.delete_fil(conn, cur)
            return edit_fil(conn, cur, name)
        elif num == '4':
            return menu_for_comp(conn, cur, name)
        else:
            print('Такого пункта в меню нет.\n')

def view_vac(conn, cur, name):
    res = hf.search_vacs_of_comp(conn, cur, name)
    if res:
        hf.render(res, vacancies.header)
        answer = input('Хотите редактировать данные вакансий? (да/нет)\n')
        print('')
        if answer == 'да':
            return edit_vac(conn, cur, name)
    else:
        print('У вас пока нет ни одного филиала, чтобы редактировать вакансии.')
        answer = input('Хотите редактировать данные филиалов? (да/нет)\n')
        print('')
        if answer == 'да':
            return edit_fil(conn, cur, name)
    return menu_for_comp(conn, cur, name)

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
            uf.add_vacancy(conn, cur)
            return edit_vac(conn, cur, name)
        elif num == '2':
            uf.change_vacancy(conn, cur)
            return edit_vac(conn, cur, name)
        elif num == '3':
            uf.delete_vacancy(conn, cur)
            return edit_vac(conn, cur, name)
        elif num == '4':
            return menu_for_comp(conn, cur, name)
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
            print('1. Поиск по данным вакансии')
            print('2. Ввести параметры поиска')
            while True:
                num = input('Выберите пункт меню: ')
                print('')
                if num == '1':
                    uf.search_by_vacancy(conn, cur, name, vacancies.header)
                    break
                elif num == '2':
                    uf.search_resume(conn, cur)
                    break
                else:
                    print('Такого пункта в меню нет.\n')
            answer = input('Вернутся в главное меню? (да/нет)\n')
            print('')
            if answer == 'нет':
                return print('До свидания!')
            else:
                return menu_for_comp(conn, cur, name)
        elif num == '2':
            name = uf.change_company(conn, cur, name)
            return menu_for_comp(conn, cur, name)
        elif num == '3':
            answer = input('Вы уверены, что хотите удалить аккаунт компании, а также все вакансии и филиалы, связанные с ней? (да/нет)\n')
            if answer == 'да':
                bf.delete(conn, cur, 'companies', 'login', name)
                return print('До свидания!')
            else:
                return menu_for_comp(conn, cur, name)
        elif num == '4':
            return view_fil(conn, cur, name)
        elif num == '5':
            return view_vac(conn, cur, name)
        elif num == '6':
            return print('До свидания!')
        else:
            print('Такого пункта в меню нет\n')

def view_resume(conn, cur, login):
    res = bf.search(conn, cur, 'resumes', ['login'], [login])
    uf.render(res, resumes.header)
    while True:
        print('Выберите дальнешее действие:')
        print('1. Изменить имеющееся резюме')
        print('2. Удалить имеющееся резюме')
        print('3. Вернутся в главное меню')
        num = input('Введите пункт меню: ')
        print('')
        if num == '1':
            uf.change_resume(conn, cur)
        elif num == '2':
            uf.delete_resume(conn, cur)
        elif num == '3':
            return menu_for_st(conn, cur, login)
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
            print('1. Поиск по данным резюме')
            print('2. Ввести параметры поиска')
            while True:
                num = input('Выберите пункт меню: ')
                print('')
                if num == '1':
                    uf.search_by_resume(conn, cur, login, resumes.header)
                    break
                elif num == '2':
                    uf.search_vacancy(conn, cur)
                    break
                else:
                    print('Такого пункта в меню нет.\n')
            answer = input('Вернутся в главное меню? (да/нет)\n')
            print('')
            if answer == 'нет':
                return print('До свидания!')
            else:
                return menu_for_st(conn, cur, login)
        elif num == '2':
            login = uf.change_user(conn, cur, login)
            return menu_for_st(conn, cur, login)
        elif num == '3':
            answer = input('Вы уверены, что хотите удалить свой аккаунт? (да/нет)\n')
            print('')
            if answer == 'да':
                bf.delete(conn, cur, 'users', 'login', login)
                return print('До свидания!')
            else:
                return menu_for_st(conn, cur, login)
        elif num == '4':
            uf.add_resume(conn, cur, login)
            return menu_for_st(conn, cur, login)
        elif num == '5':
            return view_resume(conn, cur, login)
        elif num == '6':
            return print('До свидания!')
        else:
            print('Такого пункта в меню нет.\n')

def enter(conn, cur, table):
    print('1. Авторизация')
    print('2. Регистрация')
    print('3. Выход')
    while True:
        num = input('Выберите пункт меню: ')
        print('')
        if num == '1':
            login = hf.authorization(conn, cur, table)
            print('')
            if table.name == 'companies':
                return menu_for_comp(conn, cur, login)
            return menu_for_st(conn, cur, login)
        elif num == '2':
            login, password = hf.registration(conn, cur, table)
            print('')
            if table.name == 'companies':
                uf.add_company(conn, cur, login, password)
                return menu_for_comp(conn, cur, login)
            uf.add_user(conn, cur, login, password)
            return menu_for_st(conn, cur, login)
        elif num == '3':
            return print('До свидания!')
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
            return enter(conn, cur, companies)
        elif num == '2':
            return enter(conn, cur, users)
        elif num == '3':
            return print('До свидания!')
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

if __name__ == '__main__':
    main()