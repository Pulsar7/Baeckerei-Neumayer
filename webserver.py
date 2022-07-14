"""
Bäckerei-Neumayer/Webserver/Version 2.0/Python 3.8.10
"""
from flask import (Flask)
import os,sys,argparse
sys.dont_write_bytecode = True
from src.modules import (config,request_handler)

conf = config.CONFIGURER('src/conf/config.json')
server_name = conf.get('Webserver','name')
webserver = Flask(
    server_name,
    template_folder = conf.get('Requests','template_folder'),
    static_folder = conf.get('Requests','static_folder')
)
webserver.secret_key = conf.get('Encryption','secret_key')
parser = argparse.ArgumentParser(description=server_name)
parser.add_argument('--debug',help="Debug-Mode (default=False)",default = False)
args = parser.parse_args()
request_keyword = conf.get('Requests','request_keyword')
error_request_keyword = conf.get('Requests','error_request_keyword')
responder = request_handler.REQUESTS(webserver,conf,request_keyword,error_request_keyword,server_name)
requests = conf.get('Requests')

### Requests
resp_func = None

for request in requests:
    if (request_keyword in request or error_request_keyword in request):
        myStr = request
        myVars = locals()
        myVars[myStr] = request
        exec(f"resp_func = responder.{request}") # creating 'resp_func' variable

    if (request_keyword in request):
        webserver.add_url_rule(
            rule = requests[request]['rule'], view_func = resp_func,
            methods = requests[request]['methods']
        )
    
    if (error_request_keyword in request):
        webserver.register_error_handler(int(requests[request]['rule']),resp_func)

webserver.before_request(responder.before_request)

if (__name__ == '__main__'):
    # os.system("clear") # Linux
    webserver.run(
        host = conf.get('Webserver','host'),
        port = conf.get('Webserver','port'),
        debug = args.debug
    )
