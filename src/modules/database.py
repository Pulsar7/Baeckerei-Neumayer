"""
Bäckerei Neumeyer/Database/Python 3.8.10
"""
import pymongo,sys,hashlib,os,time,random,string
from datetime import datetime

sys.dont_write_bytecode = True

class DATABASE():
    def __init__(self,logger,conf):
        (self.logger,self.conf) = (logger,conf)
        self.db_name = conf.get('Database','name')
        collections = conf.get('Database','collections')
        self.collections = collections
        connection_url = conf.get('Database','connection_url')
        dbclient = pymongo.MongoClient(connection_url) # Connects to MongoDB-Server
        self.db = dbclient[self.db_name]
        # Collections
        self.login_data = self.db[collections['LoginData']['name']]
        self.user_data = self.db[collections['UserData']['name']]
        self.tortensortiment_data = self.db[collections['TortensortimentData']['name']]
        self.contact_data = self.db[collections['ContactData']['name']]
        #

    def get_tortensortiment(self):
        mydoc = self.tortensortiment_data.find()
        sortiment = []
        for x in mydoc:
            print(x)
            sortiment.append(x)
        return sortiment

    def delete_logged_in_devices(self,session_data):
        values = self.collections['LoginData']['values']
        query = {
            values[0]: session_data[values[0]],
            values[1]: session_data[values[1]],
            values[2]: session_data[values[2]],
            values[3]: session_data[values[3]],
            values[4]: session_data[values[4]]
        }
        self.login_data.delete_many(query)
        for x in self.login_data.find():
            print(x)
    
    def check_if_logged_in(self,session_data):
        status = True
        values = self.collections['LoginData']['values']
        query = {}
        for value in values:
            if (value not in session_data):
                status = False
                break
        if (status == True):
            query = {
                values[0]: session_data[values[0]],
                values[1]: session_data[values[1]],
                values[2]: session_data[values[2]],
                values[3]: session_data[values[3]],
                values[4]: session_data[values[4]]
            }
        if (len(query) > 0):
            x = self.login_data.find_one()
            mydoc = self.login_data.find(query)
            counter = 0
            for x in mydoc:
                counter += 1
            if (counter > 0):
                end = time.time()
                start = session_data[self.collections['LoginData']['values'][3]]
                diff = (end-start)
                if (diff >= self.collections['LoginData']['max_login_time_in_sec']):
                    self.login_data.delete_one(query)
                else:
                    status = True
            else:
                status = False
        else:
            status = False
        return status

    def get_number_of_sessions(self):
        counter = 0
        for x in self.login_data.find():
            counter += 1
        return counter

    def get_number_of_users(self):
        counter = 0
        for x in self.user_data.find():
            counter += 1
        return counter

    def get_open_sessions(self):
        sessions = {}
        counter = 0
        for x in self.login_data.find():
            sessions[str(counter)] = x
            counter += 1
        return sessions

    def check_login_data(self,input_data):
        status = False
        new_session_data = {}
        clear_pwd = input_data['password']
        plaintext = clear_pwd.encode()
        d = hashlib.sha256(plaintext)
        # generate human readable hash of string
        pwd_hash = d.hexdigest()
        query = {self.collections['UserData']['values'][0]:input_data['username'],
            self.collections['UserData']['values'][1]:pwd_hash}
        mydoc = self.user_data.find(query)
        counter = 0
        for x in mydoc:
            # print(x)
            counter += 1
        if (counter > 0):
            values = self.collections['LoginData']['values']
            now = datetime.now()
            zeitpunkt = f"{now.day}.{now.month}.{now.year} - {now.hour}:{now.minute}:{now.second}"
            session_id = self.generate_session_id()
            session_key = self.generate_session_key()
            now_time = time.time()
            new_session_data = {
                values[0]: input_data['username'],
                values[1]: session_id,
                values[2]: session_key,
                values[3]: now_time,
                values[4]: zeitpunkt
            }
            self.login_data.insert_one({values[0]: input_data['username'],
                                        values[1]: session_id,
                                        values[2]: session_key,
                                        values[3]: now_time,
                                        values[4]: zeitpunkt})
            status = True
        # CHECK IF ITS IN MYDOC
        return (status,new_session_data)

    def generate_session_id(self):
        generated_id = None
        while True:
            id_elements = []
            for i in range(0,self.collections['LoginData']['session_id_len']):
                __choice = random.randint(1,2)
                if (__choice == 1):
                    id_elements.append(str(random.randint(0,9)))
                else:
                    id_elements.append(random.choice(string.ascii_lowercase))
            generated_id = "".join(id_elements)
            query = {"session_id":generated_id}
            counter = 0
            for x in self.login_data.find(query):
                counter += 1
            if (counter > 0):
                pass
            else:
                break
        return generated_id

    def generate_session_key(self):
        generated_key = None
        while True:
            key_elements = []
            for i in range(0,self.collections['LoginData']['session_key_len']):
                __choice = random.choice([1,2]) # or random.randint(1,2)
                if (__choice == 1):
                    key_elements.append(str(random.randint(0,9)))
                else:
                    key_elements.append(random.choice(string.ascii_lowercase))
            generated_key = "".join(key_elements)
            query = {"session_key":generated_key}
            counter = 0
            for x in self.login_data.find(query):
                counter += 1
            if (counter > 0):
                pass
            else:
                break
        return generated_key

    def add_contact_message(self,message_data):
        return False

