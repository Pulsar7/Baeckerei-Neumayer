"""
Bäckerei Neumeyer/Database/Python 3.8.10
"""
import pymongo,sys,hashlib,os,time,random,string
from datetime import datetime

from requests import session

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
        self.team_data = self.db[collections['TeamData']['name']]
        self.hochzeitstorten_data = self.db[collections['HochzeitstortenData']['name']]
        #

    def get_team(self):
        mydoc = self.team_data.find()
        team = {}
        counter = 0
        for x in mydoc:
            counter += 1
            team[str(counter)] = x
        sorted_team = {}
        for element in team:
            sorted_team[element] = team[str(counter)]
            counter -= 1
        if (len(team) == 0):
            sorted_team["0"] = self.collections['TeamData']['empty_data']
        return sorted_team

    def add_team_member(self,member_data):
        values = self.collections['TeamData']['values']
        query = {}
        counter = 0
        for value in values:
            query[value] = member_data[counter]
            counter += 1
        self.team_data.insert_one(query)

    def delete_team_member(self,vorname,nachname):
        counter = 0
        status = False
        values = self.collections['TeamData']['values']
        query = {values[0]:vorname,values[1]:nachname}
        for x in self.team_data.find(query):
            counter += 1
        if (counter > 0):
            self.team_data.delete_one(query)
            status = True
        return status

    def get_one_tortensortiment(self,old_torten_name):
        values = self.collections['TortensortimentData']['values']
        counter = 0
        data = None
        status = False
        for x in self.tortensortiment_data.find({values[0]:old_torten_name}):
            counter += 1
            data = x
        if (counter > 0):
            status = True
        return (status,data)

    def get_one_hochzeitstorte(self,old_torten_name):
        values = self.collections['HochzeitstortenData']['values']
        counter = 0
        data = None
        status = False
        for x in self.hochzeitstorten_data.find({values[0]:old_torten_name}):
            counter += 1
            data = x
        if (counter > 0):
            status = True
        return (status,data)

    def get_hochzeitstorten(self):
        mydoc = self.hochzeitstorten_data.find()
        torten = {}
        counter = 0
        for x in mydoc:
            counter += 1
            torten[str(counter)] = x
        sorted_torten = {}
        for element in torten:
            sorted_torten[element] = torten[str(counter)]
            counter -= 1
        if (len(torten) == 0):
            sorted_torten["0"] = self.collections['HochzeitstortenData']['empty_data']
        return sorted_torten

    def add_hochzeitstorte(self,torten_data):
        values = self.collections['HochzeitstortenData']['values']
        query = {}
        counter = 0
        for value in values:
            query[value] = torten_data[counter]
            counter += 1
        self.hochzeitstorten_data.insert_one(query)

    def update_tortensortiment(self,torten_data):
        status = False
        values = self.collections['TortensortimentData']['values']
        query = {values[0]:torten_data[0]}
        counter = 0
        old_query = None
        for x in self.tortensortiment_data.find(query):
            counter += 1
            old_query = x
        if (counter > 0):
            new_query = {
                "$set":{
                    values[0]: torten_data[1],
                    values[1]: torten_data[2],
                    values[2]: torten_data[3],
                    values[3]: torten_data[4]
                }
            }
            self.tortensortiment_data.update_one(old_query, new_query)
            status = True
        else:
            pass
        return status

    def update_hochzeitstorte(self,torten_data):
        status = False
        values = self.collections['HochzeitstortenData']['values']
        query = {values[0]:torten_data[0]}
        counter = 0
        old_query = None
        for x in self.hochzeitstorten_data.find(query):
            counter += 1
            old_query = x
        if (counter > 0):
            new_query = {
                "$set":{
                    values[0]: torten_data[1],
                    values[1]: torten_data[2],
                    values[2]: torten_data[3],
                    values[3]: torten_data[4]
                }
            }
            self.hochzeitstorten_data.update_one(old_query, new_query)
            status = True
        else:
            pass
        return status

    def remove_hochzeitstorte(self,name):
        counter = 0
        status = False
        values = self.collections['HochzeitstortenData']['values']
        query = {values[0]:name}
        for x in self.hochzeitstorten_data.find(query):
            counter += 1
        if (counter > 0):
            self.hochzeitstorten_data.delete_one(query)
            status = True
        return status

    def get_tortensortiment(self):
        mydoc = self.tortensortiment_data.find()
        sortiment = {}
        counter = 0
        for x in mydoc:
            counter += 1
            sortiment[str(counter)] = x
        sorted_sortiment = {}
        for element in sortiment:
            sorted_sortiment[element] = sortiment[str(counter)]
            counter -= 1
        if (len(sortiment) == 0):
            sorted_sortiment["0"] = self.collections['TortensortimentData']['empty_data']
        return sorted_sortiment

    def tortensortiment_add_one(self,data):
        values = self.collections['TortensortimentData']['values']
        query = {}
        counter = 0
        for value in values:
            query[value] = data[counter]
            counter += 1
        self.tortensortiment_data.insert_one(query)

    def tortensortiment_remove_one(self,name):
        counter = 0
        status = False
        values = self.collections['TortensortimentData']['values']
        query = {values[0]:name}
        for x in self.tortensortiment_data.find(query):
            counter += 1
        if (counter > 0):
            self.tortensortiment_data.delete_one(query)
            status = True
        return status

    def logout_all_devices(self,session_data):
        values = self.collections['LoginData']['values']
        for x in self.login_data.find():
            if (session_data[values[1]] != x[values[1]]):
                self.delete_logged_in_devices(x)

    def delete_other_device(self,session_id):
        values = self.collections['LoginData']['values']
        mydoc = self.login_data.find({values[1]:session_id})
        counter = 0
        for x in mydoc:
            counter += 1
        if (counter > 0):
            self.login_data.delete_one({values[1]:session_id})

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
                    self.delete_logged_in_devices(query)
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

    def get_number_of_anmerkungen(self):
        counter = 0
        for x in self.contact_data.find():
            counter += 1
        return counter

    def get_number_of_team(self):
        counter = 0
        for x in self.team_data.find():
            counter += 1
        return counter

    def get_number_of_tortensortiment(self):
        counter = 0
        for x in self.tortensortiment_data.find():
            counter += 1
        return counter

    def get_number_of_hochzeitstorten(self):
        counter = 0
        for x in self.hochzeitstorten_data.find():
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
            session_id = self.generate_id(self.collections['LoginData']['session_id_len'],self.login_data,values[1])
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
        return (status,new_session_data)

    def generate_id(self,this_len,database_col,query_element):
        generated_id = None
        while True:
            id_elements = []
            for i in range(0,this_len):
                __choice = random.randint(1,2)
                if (__choice == 1):
                    id_elements.append(str(random.randint(0,9)))
                else:
                    id_elements.append(random.choice(string.ascii_letters))
            generated_id = "".join(id_elements)
            query = {query_element:generated_id}
            counter = 0
            for x in database_col.find(query):
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
        values = self.collections['ContactData']['values']
        now = datetime.now()
        msg_id = self.generate_id(self.collections['ContactData']['msg_id_len'],self.contact_data,values[6])
        message_data[values[6]] = msg_id
        message_data[values[5]] = f"{now.day}.{now.month}.{now.year}"
        self.contact_data.insert_one(message_data)
        return True

    def delete_contact_message(self,message_id):
        status = False
        values = self.collections['ContactData']['values']
        query = {values[6]:message_id}
        counter = 0
        for x in self.contact_data.find(query):
            counter += 1
        if (counter > 0):
            self.contact_data.delete_one(query)
            status = True
        else:
            pass
        return status

    def get_anmerkungen(self):
        anmerkungen = {}
        sorted_anmerkungen = {}
        counter = 0
        for x in self.contact_data.find():
            counter += 1
            anmerkungen[str(counter)] = x
        for anmerkung in anmerkungen:
            sorted_anmerkungen[anmerkung] = anmerkungen[str(counter)]
            counter -= 1
        if (len(anmerkungen) == 0):
            sorted_anmerkungen["0"] = self.collections['ContactData']['empty_data']
        return sorted_anmerkungen

