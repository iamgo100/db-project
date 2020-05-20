'''
    base module
'''

import sqlite3

def start():
    try:
        conn = sqlite3.connect('example.db')
    except sqlite3.Error as e:
        return e
    else:
        cur = conn.cursor()
        conn.commit()
        
        status = create_tables(conn)
        return status

def create_tables(conn):
    try:
        conn.execute('PRAGMA foreign_keys = on')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS companies
                        (name TEXT PRIMARY KEY,
                        password CHAR(8) NOT NULL,
                        site TEXT NOT NULL,
                        email TEXT NOT NULL,
                        practice TEXT NOT NULL)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS filiations
                        (id INTEGER PRIMARY KEY,
                        nameOfComp TEXT NOT NULL,
                        city TEXT NOT NULL,
                        FOREIGN KEY (nameOfComp) REFERENCES companies(name) ON UPDATE CASCADE ON DELETE CASCADE)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS vacancies
                        (id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        idOfFil INTEGER NOT NULL,
                        employment TEXT,
                        pay INTEGER,
                        experience TEXT,
                        FOREIGN KEY (idOfFil) REFERENCES filiations(id) ON UPDATE CASCADE ON DELETE CASCADE)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                        (login TEXT PRIMARY KEY,
                        password CHAR(8) NOT NULL,
                        fname TEXT NOT NULL,
                        lname TEXT NOT NULL,
                        phone CHAR(11) NOT NULL,
                        city TEXT,
                        status TEXT)''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS resumes
                        (id INTEGER PRIMARY KEY,
                        login TEXT NOT NULL,
                        profession TEXT NOT NULL,
                        experience TEXT,
                        employment TEXT,
                        practice TEXT,
                        FOREIGN KEY (login) REFERENCES users(login) ON UPDATE CASCADE ON DELETE CASCADE)''')
        conn.commit()
        return 'OK'
    except sqlite3.Error as e:
        return e

if __name__ == "__main__":
    pass