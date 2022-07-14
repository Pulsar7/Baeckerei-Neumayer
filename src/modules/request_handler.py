"""
Bäckerei-Neumayer/Request-Handler/Version 2.0/Python 3.8.10
"""
import sys
from flask import (url_for, redirect, render_template, send_from_directory, session, request, flash)
sys.dont_write_bytecode = True
from src.modules import (database)

class REQUESTS():
    def __init__(self,webserver,conf,request_keyword,error_request_keyword,webserver_name):
        (self.webserver,self.conf,self.request_keyword,self.error_request_keyword) = (
            webserver,conf,request_keyword,error_request_keyword)
        (self.css_dir, self.js_dir, self.img_dir) = (
            conf.get('Requests','static_folder')+conf.get('Requests','css_route')['dir'],
            conf.get('Requests','static_folder')+conf.get('Requests','js_route')['dir'],
            conf.get('Requests','static_folder')+conf.get('Requests','img_route')['dir']
        )
        self.db = database.DATABASE(conf)
        self.webserver_name = webserver_name
        self.cookie_session_element = conf.get('Cookie-Disclaimer','cookie_session_element')
    
    def get_regular_data(self,page_name,page_type):
        data = self.conf.get('Requests','regular_data')
        data['page_name'] = page_name
        (status,msg_element) = self.db.check_if_logged_in(session)
        if (msg_element != None):
            flash(msg_element)
        data['logged_in_state'] = status
        data['error_keyword'] = self.conf.get('Alert-Messages','error_keyword')
        data['head_title'] = f"{self.webserver_name}/{self.conf.get('Requests',page_name+page_type,'head_title')}"
        data['heading_title'] = self.conf.get('Requests',page_name+page_type,'heading_title')
        data['css_files'][f'{page_name}_css_file'] = f"/css/{page_name}.css"
        if (self.cookie_session_element in session):
            data['show_cookie_disclaimer'] = False
        else:
            data['show_cookie_disclaimer'] = True
        return data
    
    #

    def before_request(self):
        pass

    # 

    def index_route(self):
        page_name = "index"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def login_route(self):
        page_name = "login"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        if (regular_data['logged_in_state'] == False):
            if (request.method == "GET"):
                pass
            else:
                username = request.form.get('username')
                password = request.form.get('password')
                status = self.db.check_user_input_data(username,password)
                if (status == True):
                    flash(self.conf.get('Alert-Messages','info','logged_in'))
                    return redirect(url_for('dashboard_route'))
                else:
                    flash(self.conf.get('Alert-Messages','errors','incorrect_username_or_pwd'))
                    return redirect(url_for('login_route'))
        else:
            return redirect(url_for('dashboard_route'))

    def dashboard_route(self):
        page_name = "login"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        if (regular_data['logged_in_state'] == True):
            return render_template(
                self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
                regular_data = regular_data
            )
        else:
            return redirect(url_for('login_route'))

    def arrival_route(self):
        page_name = "arrival"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def service_route(self):
        page_name = "service"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def contact_route(self):
        page_name = "contact"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def imprint_route(self):
        page_name = "imprint"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def team_route(self):
        page_name = "team"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def assortmentcakes_route(self):
        page_name = "assortmentcakes"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def photocakes_route(self):
        page_name = "photocakes"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )
    
    def weddingcakes_route(self):
        page_name = "weddingcakes"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def holidaycakes_route(self):
        page_name = "holodaycakes"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def easter_route(self):
        page_name = "easter"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )
    
    def christmas_route(self):
        page_name = "christmas"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    def all_saints_day_route(self):
        page_name = "all_saints_day"
        regular_data = self.get_regular_data(page_name=page_name,page_type=self.request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.request_keyword)['page_path'],
            regular_data = regular_data
        )

    # ERROR

    def not_found_error(self,*args): # 404
        page_name = "not_found"
        regular_data = self.get_regular_data(page_name,self.error_request_keyword)
        flash(self.conf.get('Alert-Messages','errors','page_not_found_404_error')%(request.url))
        return render_template(
            self.conf.get('Requests',page_name+self.error_request_keyword)['page_path'],
            regular_data = regular_data,
        )

    def bad_request_error(self,*args):
        page_name = "bad_request"
        flash(self.conf.get('Alert-Messages','errors','bad_request_400_error'))
        regular_data = self.get_regular_data(page_name,self.error_request_keyword)
        return render_template(
            self.conf.get('Requests',page_name+self.error_request_keyword)['page_path'],
            regular_data = regular_data,
        )

    # STATIC

    def css_route(self,path):
        return send_from_directory(
            self.css_dir, path
        )
    
    def js_route(self,path):
        return send_from_directory(
            self.js_dir, path
        )

    def img_route(self,path):
        return send_from_directory(
            self.img_dir, path
        )
