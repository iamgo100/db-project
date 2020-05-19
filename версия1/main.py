import sqlite3
import basefunc as bf #Подключение базовых функций
import usersfunc as uf #Подключение пользовательских функций

class companies:
    name = 'companies'
    header = '| Название | Сайт | Электронная почта | Есть ли практика для студентов |'
class filiations:
    name = 'filiations'
    header = '| ID филиала | Город |'
class vacancies:
    name = 'vacancies'
    header = '''|    ID    |  Вакансия   | Название |   ID    | Занятость | Зарплата | Опыт работы |
| вакансии | (профессия) | компании | филиала |           |          |             |'''
class resumes:
    name = 'resumes'
    header = '| ID резюме | Имя | Фамилия | Телефон | Город | Статус | Профессия | Опыт работы | Занятость | Нужна ли практика |'

def create_tables(conn):
    try:
        conn.execute('PRAGMA foreign_keys = on')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS companies
                        (name TEXT PRIMARY KEY,
                        site TEXT NOT NULL,
                        email TEXT NOT NULL,
                        practice TEXT NOT NULL)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS filiations
                        (id INTEGER PRIMARY KEY,
                        city TEXT NOT NULL)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS vacancies
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        nameOfComp TEXT NOT NULL,
                        idOfFil INTEGER NOT NULL,
                        employment TEXT,
                        pay INTEGER,
                        experience TEXT,
                        FOREIGN KEY (nameOfComp) REFERENCES companies(name) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (idOfFil) REFERENCES filiations(id) ON UPDATE CASCADE ON DELETE CASCADE)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS resumes
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fname TEXT NOT NULL,
                        sname TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        city TEXT,
                        status TEXT,
                        profession TEXT,
                        experience TEXT,
                        employment TEXT,
                        practice TEXT)''')
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f'Ошибка создания таблиц: {e}')
        return False

def edit_comp(conn, cur):
    print('Выберите действие:')
    print('1. Добавить новую компанию в реестр')
    print('2. Изменить данные имеющейся компании')
    print('3. Удалить компанию из реестра')
    print('4. Вернуться в главное меню')
    
    while True:
        num = input('Введите пункт меню: ')
        print('\n')
        if num == '1':
            values = uf.add_company()
            bf.add(conn, cur, 'companies', values)
            edit_comp(conn, cur)
            break
        elif num == '2':
            prKey = input('Введите название компании, которую хотите изменить: ')
            print('Введите новые данные для столбцов')
            print('Если не хотите изменять данные столбца, пропустите ввод, нажав Enter')
            print('\n')
            arr = uf.enter_company()
            bf.change(conn, cur, 'companies', 'name', prKey, arr[0], arr[1])
            edit_comp(conn, cur)
            break
        elif num == '3':
            prKey = input('Введите название компании, которую хотите удалить: ')
            bf.delete(conn, cur, 'companies', 'name', prKey)
            edit_comp(conn, cur)
            break
        elif num == '4':
            menu_for_comp(conn, cur)
            break
        else:
            print('Такого пункта в меню нет.\n')

def edit_fil(conn, cur):
    print('Выберите действие:')
    print('1. Добавить новый филиал в реестр')
    print('2. Изменить данные имеющегося филиала')
    print('3. Удалить филиал из реестра')
    print('4. Вернуться в главное меню')
    
    while True:
        num = input('Введите пункт меню: ')
        print('\n')
        if num == '1':
            values = uf.add_fil()
            bf.add(conn, cur, 'filiations', values)
            edit_fil(conn, cur)
            break
        elif num == '2':
            prKey = input('Введите ID филиала, который хотите изменить: ')
            print('Введите новые данные для столбцов')
            print('Если не хотите изменять данные столбца, пропустите ввод, нажав Enter')
            print('\n')
            arr = uf.enter_fil()
            bf.change(conn, cur, 'filiations', 'id', prKey, arr[0], arr[1])
            edit_fil(conn, cur)
            break
        elif num == '3':
            prKey = input('Введите ID филиала, который хотите удалить: ')
            bf.delete(conn, cur, 'filiations', 'id', prKey)
            edit_fil(conn, cur)
            break
        elif num == '4':
            menu_for_comp(conn, cur)
            break
        else:
            print('Такого пункта в меню нет.\n')
    
def edit_vac(conn, cur):
    print('Выберите действие:')
    print('1. Добавить новую вакансию в реестр')
    print('2. Изменить данные имеющейся вакансии')
    print('3. Удалить вакансию из реестра')
    print('4. Вернуться в главное меню')
    
    while True:
        num = input('Введите пункт меню: ')
        print('\n')
        if num == '1':
            values = uf.add_vacancy()
            bf.add(conn, cur, 'vacancies', values)
            edit_vac(conn, cur)
            break
        elif num == '2':
            prKey = input('Введите ID вакансии, которую хотите изменить: ')
            print('Введите новые данные для столбцов')
            print('Если не хотите изменять данные столбца, пропустите ввод, нажав Enter')
            print('\n')
            arr = uf.enter_vacancy()
            bf.change(conn, cur, 'vacancies', 'id', prKey, arr[0], arr[1])
            edit_vac(conn, cur)
            break
        elif num == '3':
            prKey = input('Введите ID вакансии, которую хотите удалить: ')
            bf.delete(conn, cur, 'vacancies', 'id', prKey)
            edit_vac(conn, cur)
            break
        elif num == '4':
            menu_for_comp(conn, cur)
            break
        else:
            print('Такого пункта в меню нет.\n')

def menu_for_comp(conn, cur):
    print('ГЛАВНОЕ МЕНЮ\n')
    print('1. Поиск резюме')
    print('2. Редактирование данных компании')
    print('3. Посмотреть имеющиеся филиалы')
    print('4. Редактирование данных филиалов')
    print('5. Посмотреть имеющиеся вакансии')
    print('6. Редактирование вакансий')
    print('7. Выход')
    
    while True:
        num = input('Выберите пункт меню: ')
        print('\n')
        if num == '1':
            print('Введите данные столбцов для поиска')
            print('Для введения нескольких параметров поиска для одного столбика,')
            print('разделяйте значения запятой и пробелом (", ")')
            print('Если хотите пропустить ввод данных столбца, нажмите Enter')
            print('\n')
            arr = uf.enter_resume()
            bf.search(conn, cur, resumes, arr)
            answer = input('Вернутся в главное меню? (y/n)\n')
            print('\n')
            if answer == 'n':
                print('До свидания!')
            else:
                menu_for_comp(conn, cur)
            break
        elif num == '2':
            edit_comp(conn, cur)
            break
        elif num == '3':
            bf.search(conn, cur, filiations, '')
            answer = input('Хотите редактировать данные филиалов? (y/n)\n')
            print('\n')
            if answer == 'y':
                edit_fil(conn, cur)
            else:
                menu_for_comp(conn, cur)
            break
        elif num == '4':
            edit_fil(conn, cur)
            break
        elif num == '5':
            bf.search(conn, cur, vacancies, '')
            answer = input('Хотите редактировать данные вакансий? (y/n)\n')
            print('\n')
            if answer == 'y':
                edit_vac(conn, cur)
            else:
                menu_for_comp(conn, cur)
            break
        elif num == '6':
            edit_vac(conn, cur)
            break
        elif num == '7':
            print('До свидания!')
            break
        else:
            print('Такого пункта в меню нет\n')

def view_resume(conn, cur):
    print('Введите ваши данные, чтобы просмотреть имеющиеся резюме')
    fname = input('Ваше имя: ')
    sname = input('Ваша фамилия: ')
    print('\n')
    columns = ['fname', 'sname']
    values = [fname, sname]
    bf.search(conn, cur, resumes, [columns, values])
    while True:
        print('Выберите дальнешее действие:')
        print('1. Изменить имеющееся резюме')
        print('2. Удалить имеющееся резюме')
        print('3. Вернутся в главное меню')
        num = input('Введите пункт меню: ')
        print('\n')
        
        if num == '1':
            prKey = input('Введите ID резюме, которое хотите изменить: ')
            print('Введите новые данные для столбцов')
            print('Если не хотите изменять данные столбца, пропустите ввод, нажав Enter')
            print('\n')
            arr = uf.enter_resume()
            bf.change(conn, cur, 'resumes', 'id', prKey, arr[0], arr[1])
        elif num == '2':
            prKey = input('Введите ID резюме, которое хотите удалить: ')
            bf.delete(conn, cur, 'resumes', 'id', prKey)
        elif num == '3':
            menu_for_st(conn, cur)
            break
        else:
            print('Такого пункта в меню нет.\n')

def menu_for_st(conn, cur):
    print('ГЛАВНОЕ МЕНЮ\n')
    print('1. Поиск вакансий')
    print('2. Добавить новое резюме')
    print('3. Посмотреть имеющиеся резюме')
    print('4. Выход')
    
    while True:
        num = input('Выберите пункт меню: ')
        print('\n')
        if num == '1':
            print('Введите данные столбцов для поиска')
            print('Для введения нескольких параметров поиска для одного столбика,')
            print('разделяйте значения запятой и пробелом (", ")')
            print('Если хотите пропустить ввод данных столбца, нажмите Enter')
            print('\n')
            arr = uf.search_vacancy(conn, cur)
            bf.search(conn, cur, vacancies, arr)
            answer = input('Вернутся в главное меню? (y/n)\n')
            print('\n')
            if answer == 'n':
                print('До свидания!')
            else:
                menu_for_st(conn, cur)
            break
        elif num == '2':
            values = uf.add_resume()
            bf.add(conn, cur, 'resumes', values)
            menu_for_st(conn, cur)
            break
        elif num == '3':
            view_resume(conn, cur)
            break
        elif num == '4':
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
            menu_for_comp(conn, cur)
            break
        elif num == '2':
            menu_for_st(conn, cur)
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
    
#             table = 'filiations'
#             prCol = 'id'
#             bf.add(conn, cur, table, [28, 'рязань'])
#             bf.change(conn, cur, table, prCol, 28, ['id'], ['29'])
#             bf.delete(conn, cur, table, prCol, 29)
#             bf.search(conn, cur, resumes, '')
#             print(uf.search_vacancy(conn, cur))
    
    conn.close()

main()