"""
Bäckerei Neumeyer/Database/Python 3.8.10
"""
import pymongo,sys,hashlib,os

sys.dont_write_bytecode = True

class DATABASE():
    def __init__(self,logger,conf):
        (self.logger,self.conf) = (logger,conf)
        self.db_name = conf.get('Database','name')
        collections = conf.get('Database','collections')
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
        for x in mydoc:
            print(x)
        return mydoc
    
    def check_if_logged_in(self,session_data):
        # session_data = {"session_key":"","session_id":"","username":""}
        mydoc = self.login_data.find(session_data)
        for x in mydoc:
            print(x)
        # CHECK IF ITS ALREADY IN MYDOC
        return False

    def check_login_data(self,input_data):
        clear_pwd = input_data['password']
        plaintext = clear_pwd.encode()
        d = hashlib.sha256(plaintext)
        # generate human readable hash of string
        pwd_hash = d.hexdigest()
        query = {"username":input_data['username'],"password":pwd_hash}
        mydoc = self.user_data.find(query)
        for x in mydoc:
            print(x)
        # CHECK IF ITS IN MYDOC

    def add_contact_message(self,message_data):
        return False

