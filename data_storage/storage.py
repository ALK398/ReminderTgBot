import csv
import pandas as pd
import os


def anaot(login, password):  # add_new_account_on_table
    name_table = f'data_storage/user_tables/{login}_table.csv'
    sp_log = [login, password, name_table]
    data = ['login', 'password', 'name_table']
    with open('data_storage/other_tables/logs.csv', 'a+', newline='') as f:
        if os.stat('data_storage/other_tables/logs.csv').st_size == 0:
            writer = csv.DictWriter(f, fieldnames=data, delimiter=';')
            writer.writeheader()
        writer = csv.writer(f, delimiter=';')
        writer.writerow(sp_log)


def antot(login, mission_type, title, text, date='', status=''):  # add_new_mission_on_table
    if mission_type == 'task':
        status = 'False'
    data = ['login', 'mission_type', 'title', 'text', 'date', 'status']
    with open(f'data_storage/user_tables/{login}_table.csv', 'a+', newline='') as f:
        if os.stat(f'data_storage/user_tables/{login}_table.csv').st_size == 0:
            writer = csv.DictWriter(f, fieldnames=data, delimiter=';')
            writer.writeheader()
        writer = csv.writer(f, delimiter=';')
        writer.writerow([mission_type, title, text, date, status])


def view_mission(login, number_mission):
    with open(f'data_storage/user_tables/{login}_table.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        b = []
        for row in spamreader:
            b.append(row)
        return f'тип:{b[number_mission][0]}\nназвание:{b[number_mission][1]}\nописание:{b[number_mission][2]}\nдата:{b[number_mission][3]}\nдата:{b[number_mission][3]}\nстатус:{b[number_mission][4]}'


def view_missions(login):
    with open(f'data_storage/user_tables/{login}_table.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        next(spamreader)
        b = []
        d = {
            'note': 'заметка',
            'reminder': 'напоминание',
            'task': 'задача',
             }
        for row in spamreader:
            if row[3] == '' and row[4] == '':
                b.append(f'название: {row[1]}\nтип: {d[row[0]]}\nописание: {row[2]}')
            elif row[4] == '':
                b.append(f'название: {row[1]}\nтип: {d[row[0]]}\nописание: {row[2]}\nдата: {row[3]}')
            else:
                b.append(f'название: {row[1]}\nтип: {d[row[0]]}\nописание: {row[2]}\nдата: {row[3]}\nстатус: {row[4]}')
        return b


print(view_missions('albert'))


def read_table_with_account():
    df = pd.read_csv('data_storage/other_tables/logs.csv', sep=';')
    return df


def read_account_table(login):
    df = pd.read_csv(f'data_storage/user_tables/{login}_table.csv', sep=';')
    return df


def edit_title(login, number_row, title):
    df = pd.read_csv(f'data_storage/user_tables/{login}_table.csv', sep=';')
    df.ix[number_row, 1] = title


def edit_text(login, number_row, text):
    df = pd.read_csv(f'data_storage/user_tables/{login}_table.csv', sep=';')
    df.ix[number_row, 2] = text


def edit_date(login, number_row, new_date):
    df = pd.read_csv(f'data_storage/user_tables/{login}_table.csv', sep=';')
    df.ix[number_row, 3] = new_date


def edit_status(login, number_row, status):
    df = pd.read_csv(f'data_storage/user_tables/{login}_table.csv', sep=';')
    df.ix[number_row, 4] = status


def edit_password(number_acc, new_password):
    df = pd.read_csv(f'data_storage/other_tables/logs.csv', sep=';')
    df.ix[number_acc, 1] = new_password
