import os
import json
import datetime

if os.path.isfile("db.json"):
    print("db.json exists\nCODE 0 OK")
else:
    print("db.json doesn't exist\nCODE 1 ERROR\nCreating db file..")
    try:
        open("db.json", "w", encoding='utf-8').close()
    except:
        print("db.json can't be created\nCODE 1 ERROR")
    print("db.json created\nCODE 0 OK")
class UserException(Exception):
    pass

class DatabaseInteraction:
    def __init__(self, db_file='db.json'):
        self.db_file = db_file
    
    def generate_chat_profile(self, chat_id, words_count, words):
        data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        if chat_id not in data:
            data[chat_id] = {}
            data[chat_id]["words_count"] = words_count
            data[chat_id]["words"] = words
            try:
                with open(self.db_file, 'w') as f:
                    json.dump(data, f, indent=4)
                    return True
            except:
                return False
            raise UserException(f"Chat {chat_id} doesn't exist. Adding chat to database..")
        else:
            raise UserException(f"Chat {chat_id} already exists.")
    def add_text_data(self, chat_id, text_data):
        data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        if chat_id not in data:
            raise UserException(f"Chat {chat_id} doesn't exist.")
        words_data = data[chat_id]["words"]
        filtred_data = text_data.replace(',','').replace('.','').strip()
        if len(filtred_data) > 200:
            first_part = filtred_data[:int(len(filtred_data) / 2)]
            second_part = filtred_data[int(len(filtred_data) / 2):]
            if len(first_part) > 100:
                third_part = first_part[:int(len(first_part) / 2)]
                fourth_part = first_part[int(len(first_part) / 2):]
                words_data.append(third_part)
                words_data.append(fourth_part)
                data[chat_id]["words_count"] += 2
            else:
                words_data.append(first_part)
                words_data.append(second_part)
                data[chat_id]["words_count"] += 2
            if len(second_part) > 100:
                fifth_part = second_part[:int(len(second_part) / 2)]
                sixth_part = second_part[int(len(second_part) / 2):]
                words_data.append(fifth_part)
                words_data.append(sixth_part)
                data[chat_id]["words_count"] += 2
            else:
                words_data.append(first_part)
                words_data.append(second_part)
                data[chat_id]["words_count"] += 2
        else:
            words_data.append(filtred_data)
            data[chat_id]["words_count"] += 1
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)
    def get_chat_message_count(self, chat_id):
        data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        if chat_id not in data:
            raise UserException(f"Chat {chat_id} doesn't exist.")
        return data[chat_id]["words_count"]
    def get_chat_messages(self, chat_id):
        data = {}
        if os.path.isfile(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        if chat_id not in data:
            raise UserException(f"Chat {chat_id} doesn't exist.")
        return data[chat_id]["words"]
