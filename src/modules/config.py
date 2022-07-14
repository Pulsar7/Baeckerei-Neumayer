"""
Bäckerei-Neumayer/Config/Version 2.0/Python 3.8.10
"""
import sys,json

sys.dont_write_bytecode = True

class CONFIGURER():
    def __init__(self,path):
        self.path = path
        
    def get(self,*args):
        with open(self.path,'r') as json_file_data:
            data = json.load(json_file_data)
            for arg in args:
                data = data[arg]
        return data

    def get_db(self,*args):
        with open(self.get('Database','config_file'),'r') as json_file_data:
            data = json.load(json_file_data)
            for arg in args:
                data = data[arg]
        return data
        
    
