'''
    Вспомогательные функции
    alert - процерура оповещения пользователя, как вводить данные
    render - процедура вывода результата поиска данных в бд
    cycle - функция ввода обязательного параметра
    add_values_to_arrays - функция ввода параметров
    if_empty - функция проверки ввода на заполненность
    search_id - функция генерации уникального id
    authorization - авторизация пользователя
    registration - регистрация пользователя
    making_vac_entries - составление записи вакансии для поиска
'''
import basefunc as bf # Подключение базовых функций

def alert(action):
    if action == 'add':
        print('Введите данные для каждого столбца')
        print('Если хотите пропустить ввод данных столбца, нажмите Enter')
        print('Обязательные поля помечены звездочкой *')
    elif action == 'change':
        print('Введите новые данные для столбцов')
        print('Если не хотите изменять данные столбца, пропустите ввод, нажав Enter')
    elif action == 'search':
        print('Введите данные столбцов для поиска')
        print('Для введения нескольких параметров поиска для одного столбика,')
        print('разделяйте значения запятой и пробелом (", ")')
        print('Если хотите пропустить ввод данных столбца, нажмите Enter')
    print('')

def render(entries, header):
    if not entries:
        print('По вашему запросу ничего не найдено')
    else:
        size = 0
        lenH = len(header)
        for h in header:
            if h is not '\n':
                size += len(h) + 3
            else:
                lenH = int((len(header) - 1)/2)
                break
        delim = '  ' + '-' * (size - 1)

        strH = ' | '.join(header)
        print(f' | {strH} |')
        print(delim)

        for entry in entries:
            arrE = []
            for i in range(lenH):
                l = len(header[i])
                arg = str(entry[i])
                if len(arg) > l:
                    arrE.append(arg[:l - 2] + '..')
                else:
                    arrE.append('{:^{w}}'.format(arg, w = l))
            strE = ' | '.join(arrE)
            print(f' | {strE} |')
            print(delim)
    print('')

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

def search_id(conn, cur, table):
    res = bf.search(conn, cur, table, [], [])
    return len(res) + 1

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

def registration(conn, cur, table):
    if table.name == 'companies':
        while True:
            login = input('Введите название компании (далее оно будет использоваться как ваш логин для входа в систему): ')
            if not bf.search(conn, cur, 'companies', ['login'], [login]):
                while True:
                    password = input('Придумайте восьмизначный пароль: ')
                    if len(password) == 8:
                        return login, password
                    else:
                        print('В пароле должно быть 8 символов!')
            else:
                print('Компания с таким названием уже существует.')
    else:
        while True:
            login = input('Придумайте логин: ')
            if not bf.search(conn, cur, 'users', ['login'], [login]):
                while True:
                    password = input('Придумайте восьмизначный пароль: ')
                    if len(password) == 8:
                        return login, password
                    else:
                        print('В пароле должно быть 8 символов!')
            else:
                print('Пользователь с таким логином уже существует.')

def making_vac_entries(conn, cur, columns_v, values_v, columns_c, values_c, columns_cm, values_cm):
    inf = []
    entries = []
    companies = bf.search(conn, cur, 'companies', columns_cm, values_cm)
    filiations = bf.search(conn, cur, 'filiations', columns_c, values_c)
    for fil in filiations:
        for comp in companies:
            if fil[1] == comp[0]:
                columns_v.append('idOfFil')
                values_v.append(fil[0])
                inf.append((fil[0], fil[2], comp[0], comp[2], comp[3], comp[4]))
                break
    vacancies = bf.search(conn, cur, 'vacancies', columns_v, values_v)
    if vacancies:
        for vac in vacancies:
            for i in inf:
                if vac[2] == i[0]:
                    entry = (vac[0], vac[1], i[1], vac[3], vac[4], vac[5], i[2], i[3], i[4], i[5])
                    entries.append(entry)
                    break
    header = ['   ID   ', '  Профессия  ', '  Город  ', 'Занятость', 'Зарплата', '    Опыт    ', '    Название    ', '    Сайт    ', '   Электронная   ', 'Есть ли ', '\n',
              'вакансии', '             ', '         ', '         ', '        ', '   работы   ', '    компании    ', '            ', '      почта      ', 'практика']
    render(entries, header)

def making_res_entries(conn, cur, columns_u, values_u, columns_r, values_r):
    entries = []
    users = bf.search(conn, cur, 'users', columns_u, values_u)
    for user in users:
        columns_r.append('login')
        values_r.append(user[0])
    if columns_r and values_r:
        resumes = bf.search(conn, cur, 'resumes', columns_r, values_r)
        if resumes:
            for resume in resumes:
                user = bf.search(conn, cur, 'users', ['login'], [resume[1]])
                user = user[0]
                entry = (resume[0], user[2], user[3], user[4], user[5], user[6], resume[2], resume[3], resume[4], resume[5])
                entries.append(entry)
    header = ['  ID  ', '     Имя     ', '   Фамилия   ', '   Номер   ', '  Город  ', '  Статус  ', '   Профессия   ', '    Опыт    ', 'Занятость', 'Нужна ли', '\n',
              'резюме', '             ', '             ', ' телефона  ', '         ', '          ', '               ', '   работы   ', '         ', 'практика']
    render(entries, header)

def search_vacs_of_comp(conn, cur, name):
    fils = bf.search(conn, cur, 'filiations', ['nameOfComp'], [name])
    if fils:
        columns = []
        values = []
        for fil in fils:
            columns.append('idOfFil')
            values.append(fil[0])
        res = bf.search(conn, cur, 'vacancies', columns, values)
        return res

if __name__ == '__main__':
    pass