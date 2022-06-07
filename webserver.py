"""
Bäckerei Neumeyer/Webserver/Python 3.8.10
"""
import sys,logging,argparse,os,hashlib
sys.dont_write_bytecode = True
from flask import (Flask)
from src.modules import (config,request_handler,database)

conf = config.CONFIG('src/conf/config.json')
webserver_name = conf.get('Webserver','name')
logger = logging.getLogger(webserver_name)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(conf.get('Logging','formatter'))
ch.setFormatter(formatter)
logger.addHandler(ch)
webserver = Flask(
    webserver_name,
    template_folder = conf.get('Webserver','template_folder'),
    static_folder = conf.get('Webserver','static_folder')
)
webserver.secret_key = conf.get('Webserver','secret_key')
db = database.DATABASE(logger,conf)
requests = request_handler.REQUESTS(logger,conf,db,webserver_name)
args = ""

########
# Templates
index_route = conf.get('Requests','index_route')
about_route = conf.get('Requests','about_route')
service_route = conf.get('Requests','service_route')
anfahrt_route = conf.get('Requests','anfahrt_route')
kontakt_route = conf.get('Requests','kontakt_route')
impressum_route = conf.get('Requests','impressum_route')
login_route = conf.get('Requests','login_route')
tortensortiment_route = conf.get('Requests','tortensortiment_route')
dashboard_route = conf.get('Requests','dashboard_route')
logout_route = conf.get('Requests','logout_route')

webserver.add_url_rule(rule = index_route['rule'], view_func = requests.index_route, 
    methods = index_route['methods'])
webserver.add_url_rule(rule = about_route['rule'], view_func = requests.about_route, 
    methods = about_route['methods'])
webserver.add_url_rule(rule = service_route['rule'], view_func = requests.service_route, 
    methods = service_route['methods'])
webserver.add_url_rule(rule = anfahrt_route['rule'], view_func = requests.anfahrt_route, 
    methods = anfahrt_route['methods'])
webserver.add_url_rule(rule = kontakt_route['rule'], view_func = requests.kontakt_route, 
    methods = kontakt_route['methods'])
webserver.add_url_rule(rule = impressum_route['rule'], view_func = requests.impressum_route, 
    methods = impressum_route['methods'])
webserver.add_url_rule(rule = login_route['rule'], view_func = requests.login_route, 
    methods = login_route['methods'])
webserver.add_url_rule(rule = tortensortiment_route['rule'], view_func = requests.tortensortiment_route, 
    methods = tortensortiment_route['methods'])
webserver.add_url_rule(rule = dashboard_route['rule'], view_func = requests.dashboard_route, 
    methods = dashboard_route['methods'])
webserver.add_url_rule(rule = logout_route['rule'], view_func = requests.logout_route,
    methods = logout_route['methods']
)


# Errors/Func
not_found_route = conf.get('Requests','404_route')
bad_request_route = conf.get('Requests','400_route')

webserver.register_error_handler(int(not_found_route['rule']),requests.not_found_route)
webserver.register_error_handler(int(bad_request_route['rule']), requests.bad_request_route)

# Static
css_route = conf.get('Requests','css_route')
js_route = conf.get('Requests','js_route')
img_route = conf.get('Requests','img_route')

webserver.add_url_rule(rule = css_route['rule'], view_func = requests.css_route, 
    methods = css_route['methods'])
webserver.add_url_rule(rule = js_route['rule'], view_func = requests.js_route, 
    methods = js_route['methods'])
webserver.add_url_rule(rule = img_route['rule'], view_func = requests.img_route, 
    methods = img_route['methods'])
########

if (__name__ == '__main__'):
    os.system("clear") # Linux
    webserver.run(
        host = conf.get('Webserver','host'),
        port = conf.get('Webserver','port'),
        debug = True
        # debug = args.debug
    )
