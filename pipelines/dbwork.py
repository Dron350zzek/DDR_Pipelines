import sqlite3
import csv
import pandas

## http://hello.com/home --> hello.com
def get_domain(url):
    return url.split("://")[1].split("/")[0]


def execSQL(query, connection='db.db'):
    db = sqlite3.connect(connection)
    db.execute(query)
    db.commit()
    db.close()


def create(table, query, connection='db.db'):
    db = sqlite3.connect(connection)
    db.create_function("domain_of_url", 1, get_domain)
    db.execute("create table if not exists " + table + " as " + query)
    db.close()
    

def save(file, table, connection='db.db'):
    with open(f"{file}.csv", "w", newline='') as file:
        cursor = sqlite3.connect(connection).cursor()
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'url', 'domain_of_url'])
        data = cursor.execute("SELECT * FROM " + table)
        writer.writerows(data)


def load(file, table, connection='db.db'):
    db = sqlite3.connect(connection)
    pandas.read_csv(f'{file}').to_sql(name=table, con=db, if_exists='append', index=False)
    db.close()