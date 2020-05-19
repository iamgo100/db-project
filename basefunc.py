'''
    Базовые функции для манипуляции базой данных
    1. добавление записи в бд
    2. изменение записи бд
    3. удаление записи из бд
    4. поиск записи в бд
'''
import sqlite3

def add(conn, cur, table, values):
    params = '('
    for i in range(len(values) - 1):
        params = params + '?, '
    params = params + '?)'
    query = f'INSERT INTO {table} VALUES {params}'
    try:
        cur.execute(query,values)
    except sqlite3.Error as e:
        print(f'Ошибка добавления: {e}\n')
    else:
        print('Запись успешно добавлена\n')
        conn.commit()

def verify_existence(conn, cur, table, column, value):
    res = cur.execute(f'SELECT * FROM {table} WHERE {column} = "{str(value)}"').fetchall()
    if res == []:
        return False
    else:
        return True

def change(conn, cur, table, prCol, prKey, columns, values):
    num = min(len(columns),len(values))
    columnsStr = ''
    params = ''
    for i in range(num - 1):
        columnsStr = columnsStr + f'{columns[i]}, '
        params = params + '?, '
    query = f'UPDATE {table} SET ({columnsStr}{columns[num - 1]}) = ({params}?) WHERE {prCol} = "{str(prKey)}"'
    try:
        cur.execute(query,values)
    except sqlite3.Error as e:
        print(f'Ошибка изменения: {e}\n')
    else:
        print('Запись успешно изменена\n')
        conn.commit()
        
def delete(conn, cur, table, column, value):
    query = f'DELETE FROM {table} WHERE {column} = "{str(value)}"'
    try:
        cur.execute(query)
    except sqlite3.Error as e:
        print(f'Ошибка удаления: {e}\n')
    else:
        print('Запись успешно удалена\n')
        conn.commit()
        
def search(conn, cur, table, arg):
    query = f'SELECT * FROM {table.name}'
    if type(arg) == list:
        columns = arg[0]
        values = arg[1]
        if columns != [] or values != []:
            query = query + ' WHERE ('
            num = min(len(columns),len(values))
        else:
            num = 0
        for i in range(num):
            query = query + f'{columns[i]} = "{str(values[i])}"'
            if i != num - 1:
                if columns[i] == columns[i+1]:
                    query = query + ' OR '
                else:
                    query = query + f' OR {columns[i]} = "-") AND ('
            else:
                query = query + f' OR {columns[num - 1]} = "-")'
    else:
        query = query + arg
    try:
        res = cur.execute(query).fetchall()
    except sqlite3.Error as e:
        print(f'Ошибка поиска: {e}\n')
    else:
        if res == []:
            print('По вашему запросу ничего не найдено\n')
        else:
            print(table.header)
            for i in range(len(res)):
                print(res[i])
            print('')
        conn.commit()
        
if __name__ == '__main__':
    pass