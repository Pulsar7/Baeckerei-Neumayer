"""
Bäckerei-Neumayer/Pymongo-Database/Version 2.0/Python 3.8.10
"""
import sys,pymongo,hashlib
sys.dont_write_bytecode = True

class DATABASE():
    def __init__(self,conf):
        collections = conf.get_db('Collections')
        (self.conf,self.collections) = (conf,collections)
        connection_url = conf.get_db('Connection','connection_url')
        dbclient = pymongo.MongoClient(connection_url) # Connects to MongoDB-Server
        db_name = conf.get_db('Connection','db_name')
        self.db = dbclient[db_name]
        # Collections
        self.session_data = self.db[collections['SessionData']['name']]
        self.user_data = self.db[collections['UserData']['name']]
        self.weddingcake_data = self.db[collections['WeddingcakeData']['name']]
        self.assortmentcake_data = self.db[collections['AssortmentcakeData']['name']]
        self.christmascake_data = self.db[collections['ChristmascakeData']['name']]
        self.photocakes_data = self.db[collections['PhotocakesData']['name']]
        #

    def check_if_logged_in(self,session_data):
        values = self.collections['SessionData']['values']
        (status,msg_element,query) = (True,None,{})
        for value in values:
            if (value not in session_data):
                status = False
                # msg_element = self.conf.get('Alert-Messages','errors','missing_value_in_session_data')%(value)
                status = False
                break
            else:
                query[value] = session_data[value]
        if (status == True):
            counter = 0
            for x in self.session_data.find(query):
                counter += 1
            if (counter > 0):
                status = True # not necessary
            else:
                status = False
                msg_element = self.conf.get('Alert-Messages','errors','invalid_session_data')
        return (status,msg_element)

    def check_user_input_data(self,username,password):
        (status,counter,user_query) = (False,0,None)
        values = self.collections['UserData']['values']
        for x in self.user_data.find({values[0]: username}):
            counter += 1
            user_query = x
        if (counter > 0):
            db_pwd = user_query[values[1]] # hashed password from database
            plaintext_pwd = password.encode() # bytes password from user input
            d = hashlib.sha256(plaintext_pwd)
            hashed_pwd = d.hexdigest()
            if (hashed_pwd == db_pwd):
                status = True
        return status

    # Delete from collection

    def delete_element_from_collection(self,element_id,collection_name,db_variable):
        values = self.collections[collection_name]['values']
        query = {values[0]:element_id}
        (status,msg_element) = (False,None)
        state = db_variable.delete_one(query)
        print(state)
        if (status == False):
            msg_element = self.conf.get('Alert-Messages','errors','could_not_delete_element_from_db')%(element_id,
                collection_name)
        else:
            msg_element = self.conf.get('Alert-Messages','info','deleted_element_from_db')%(element_id)
        return (status,msg_element)

    def delete_cake_from_weddingcakes(self,cake_id):
        return self.delete_element_from_collection(cake_id,"WeddingcakeData",self.weddingcake_data)

    def delete_cake_from_assortmentcakes(self,cake_id):
        return self.delete_element_from_collection(cake_id,"AssortmentcakeData",self.assortmentcake_data)

    def delete_cake_from_photocakes(self,cake_id):
        return self.delete_element_from_collection(cake_id,"PhotocakesData",self.photocakes_data)

    def delete_cake_from_christmascakes(self,cake_id):
        return self.delete_element_from_collection(cake_id,"ChristmascakeData",self.christmascake_data)

    # Get from collection

    def get_all_users(self):
        all_users = {}
        counter = 0
        for user in self.user_data.find({}):
            counter += 1
            all_users[str(counter)] = user
        all_sorted_users = {}
        number = counter
        for user in all_users:
            all_sorted_users[user] = all_users[str(counter)]
            counter -= 1
        return (number,all_users)
