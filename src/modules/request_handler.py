"""
Bäckerei Neumeyer/Request Handler/Python 3.8.10
"""
import sys
from flask import (render_template, redirect, send_from_directory, request, url_for)
sys.dont_write_bytecode = True

class REQUESTS():
    def __init__(self,logger,conf,db,webserver_name):
        (self.logger,self.conf,self.db,self.webserver_name) = (logger,conf,db,webserver_name)
        self.regular_data = conf.get('Requests','regular_data')
    
    def get_regular_resp_data(self,page_name):
        data = self.regular_data
        data['page_path'] = self.conf.get('Requests',f'{page_name}_route')['page_path']
        data['css_files']['page_css_file'] = f"/css/{page_name}.css"
        data['head_title'] = self.webserver_name+"/"+self.conf.get('Requests',f'{page_name}_route')['head_title']
        data['heading_title'] = self.conf.get('Requests',f'{page_name}_route')['heading_title']
        # data['page_js_file'] = f"/js/{page_name}.js"
        return data

    def index_route(self):
        name = "index"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data,
            welcome_front_text = ""
        )

    def about_route(self):
        name = "about"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data
        )

    def service_route(self):
        name = "service"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data
        )

    def anfahrt_route(self):
        name = "anfahrt"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data
        )

    def kontakt_route(self):
        name = "kontakt"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data
        )

    def impressum_route(self):
        name = "impressum"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data
        )

    def login_route(self):
        name = "login"
        if (request.method == "GET"):
            regular_data = self.get_regular_resp_data(name)
            return render_template(
                regular_data['page_path'],
                regular_data = regular_data
            )
        else: # Handle Post-Request
            return redirect(url_for('login_route'))

    def not_found_route(self,*args):
        name = "404"
        requested_url = request.url
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data,
            requested_url = requested_url
        )

    def bad_request_route(self,*args):
        name = "400"
        requested_url = request.url
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data,
            requested_url = requested_url
        )

    # Static

    def css_route(self,path):
        return send_from_directory(
            self.conf.get('Requests','css_route')['directory'], path
        )

    def js_route(self,path):
        return send_from_directory(
            self.conf.get('Requests','js_route')['directory'], path
        )

    def img_route(self,path):
        return send_from_directory(
            self.conf.get('Requests','img_route')['directory'], path
        )