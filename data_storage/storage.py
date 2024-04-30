import os, datetime

import csv
import pandas as pd


def anaot(login, password):  # add_new_account_on_table
    sp_log = [login, password]
    data = ['login', 'password']
    with open(f'data_storage/user_tables/{login}_notes.csv', 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'text'], delimiter=';')
        writer.writeheader()
    with open(f'data_storage/user_tables/{login}_reminders.csv', 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'text', 'date'], delimiter=';')
        writer.writeheader()
    with open('data_storage/other_tables/logs.csv', 'a+', newline='') as f:
        if os.stat('data_storage/other_tables/logs.csv').st_size == 0:
            writer = csv.DictWriter(f, fieldnames=data, delimiter=';')
            writer.writeheader()
        writer = csv.writer(f, delimiter=';')
        writer.writerow(sp_log)


def antot(login, mission_type, title, text, date='', chat_id=''):  # add_new_mission_on_table
    data = ''
    if mission_type == 'note':
        data = [title, text]
    if mission_type == 'reminder':
        data = [title, text, date, chat_id]
    with open(f'data_storage/user_tables/{login}_{mission_type}s.csv', 'a+', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)


def read_table_with_account():
    df = pd.read_csv('data_storage/other_tables/logs.csv', sep=';')
    return df


def view_mission(login):
    with open(f'data_storage/user_tables/{login}_notes.csv', newline='') as csvfile:
        spamreader1 = csv.reader(csvfile, delimiter=';')
        notes_sp = []
        next(spamreader1)
        for row in spamreader1:
            notes_sp.append(row)
    with open(f'data_storage/user_tables/{login}_reminders.csv', newline='') as csvfile:
        spamreader2 = csv.reader(csvfile, delimiter=';')
        reminders_sp = []
        next(spamreader2)
        for row in spamreader2:
            reminders_sp.append(row)
    sp = notes_sp + reminders_sp
    return sp


def delete_mission(login, title):
    with open(f'data_storage/user_tables/{login}_notes.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        next(spamreader)
        i = 0
        for row in spamreader:
            if row[0] == title:
                df = pd.read_csv(f'data_storage/user_tables/{login}_notes.csv')
                df = df.drop(i)
                df.to_csv(f'data_storage/user_tables/{login}_notes.csv', index=False)
                i += 1
    with open(f'data_storage/user_tables/{login}_reminders.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        next(spamreader)
        i = 0
        for row in spamreader:
            if row[0] == title:
                df = pd.read_csv(f'data_storage/user_tables/{login}_reminders.csv')
                df = df.drop(i)
                df.to_csv(f'data_storage/user_tables/{login}_reminders.csv', index=False)
                i += 1


def check_reminders():
    now = datetime.datetime.now()
    sp = []
    with open(f'data_storage/other_tables/logs.csv', newline='') as csvfile:
        spamreader1 = csv.reader(csvfile, delimiter=';')
        next(spamreader1)
        for login in spamreader1:
            with open(f'data_storage/user_tables/{login[0]}_reminders.csv', newline='') as csvfile:
                spamreader2 = csv.reader(csvfile, delimiter=';')
                next(spamreader2)
                for row in spamreader2:
                    if row[-2] <= now:
                        sp.append(row)
                        delete_mission(login, row[0])
    return sp


def search_login(login):
    with open(f'data_storage/other_tables/logs.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        next(spamreader)
        for row in spamreader:
            if row[0] == login:
                return True
        return False


def search_password(login, password):
    with open(f'data_storage/other_tables/logs.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        next(spamreader)
        for row in spamreader:
            if row[0] == login and row[1] == password:
                return True
        return False


def read_account_tables(login):
    df1 = pd.read_csv(f'data_storage/user_tables/{login}_notes.csv', sep=';')
    df2 = pd.read_csv(f'data_storage/user_tables/{login}_reminders.csv', sep=';')
    return df1, df2


def edit_title(login, mission_type, number_row, title):
    df = pd.read_csv(f'data_storage/user_tables/{login}_{mission_type}s.csv', sep=';')
    df.ix[number_row, 1] = title


def edit_text(login, mission_type, number_row, text):
    df = pd.read_csv(f'data_storage/user_tables/{login}_{mission_type}s.csv', sep=';')
    df.ix[number_row, 2] = text


def edit_date(login, mission_type, number_row, new_date):
    df = pd.read_csv(f'data_storage/user_tables/{login}_{mission_type}s.csv', sep=';')
    df.ix[number_row, 3] = new_date
