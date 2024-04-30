import json


def reset_info():
    with open('data_storage/temporary_sessions/user_informations.json', 'w') as f:
        json.dump({
            "username": [
                {
                    "user_logs": [
                        {
                            "login": ""
                        },
                        {
                            "password": ""
                        }
                    ]
                },
                {
                    "mission": [
                        {
                            "mission_type": ""
                        },
                        {
                            "mission_title": ""
                        },
                        {
                            "mission_description": ""
                        },
                        {
                            "mission_date": ""
                        }
                    ]
                }
            ]
        }, f, indent=4)


def fill_login(user_name, login):
    with open('data_storage/temporary_sessions/user_informations.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)

        if user_name not in data:
            data[user_name] = [
                {
                    "user_logs": [
                        {
                            "login": ""
                        },
                        {
                            "password": ""
                        }
                    ]
                },
                {
                    "mission": [
                        {
                            "mission_type": ""
                        },
                        {
                            "mission_title": ""
                        },
                        {
                            "mission_description": ""
                        },
                        {
                            "mission_date": ""
                        }
                    ]
                }
            ]
        data[user_name][0]["user_logs"][0]["login"] = str(login)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)


def fill_password(user_name, password):
    with open('data_storage/temporary_sessions/user_informations.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data[user_name][0]["user_logs"][1]["password"] = str(password)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)


def fill_mission_type(user_name, mission_type):
    with (open('data_storage/temporary_sessions/user_informations.json', 'r+', encoding='utf-8') as f):
        data = json.load(f)
        data[user_name][1]["mission"][0]["mission_type"] = str(mission_type)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)


def fill_mission_title(user_name, mission_title):
    with open('data_storage/temporary_sessions/user_informations.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data[user_name][1]["mission"][1]["mission_title"] = str(mission_title)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)


def fill_mission_description(user_name, mission_description):
    with open('data_storage/temporary_sessions/user_informations.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data[user_name][1]["mission"][2]["mission_description"] = str(mission_description)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)


def fill_mission_date(user_name, mission_date):
    with open('data_storage/temporary_sessions/user_informations.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data[user_name][1]["mission"][3]["mission_date"] = str(mission_date)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_info(user_name, elem):
    with open('data_storage/temporary_sessions/user_informations.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        if elem == 'login':
            return data[user_name][0]["user_logs"][0]["login"]
        if elem == 'password':
            return data[user_name][0]["user_logs"][1]["password"]
        if elem == 'mission_type':
            return data[user_name][1]["mission"][0]["mission_type"]
        if elem == 'mission_title':
            return data[user_name][1]["mission"][1]["mission_title"]
        if elem == 'mission_description':
            return data[user_name][1]["mission"][2]["mission_description"]
        if elem == 'mission_date':
            return data[user_name][1]["mission"][3]["mission_date"]
