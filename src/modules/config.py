"""
Bäckerei Neumeyer/Config/Python 3.8.10
"""
import sys,json

sys.dont_write_bytecode = True

class CONFIG():
    def __init__(self,path):
        self.path = path
        
    def get(self,category,name):
        with open(self.path,'r') as json_file_data:
            data = json.load(json_file_data)[category][name]
        return data
    
