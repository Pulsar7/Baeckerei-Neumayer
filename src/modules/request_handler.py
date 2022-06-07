"""
Bäckerei Neumeyer/Request Handler/Python 3.8.10
"""
import sys
from flask import (render_template, redirect, send_from_directory, request, url_for, session, flash)
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
            regular_data = regular_data
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
        if (request.method == "GET"):
            regular_data = self.get_regular_resp_data(name)
            return render_template(
                regular_data['page_path'],
                regular_data = regular_data
            )
        else:
            vorname = request.form.get('vorname')
            nachname = request.form.get('nachname')
            telefon = request.form.get('telefon')
            email = request.form.get('email')
            anmerkung = request.form.get('anmerkung')
            checkbox = request.form.get('checkbox') # don't have to check this value
            # validates email and phone number
            unknown_email_chars = self.conf.get('Requests','kontakt_route')['unknown_characters']
            needed_email_chars = self.conf.get('Requests','kontakt_route')['email_validation']
            alert_messages = self.conf.get('Requests','kontakt_route')['alert_messages']
            valid = True
            for element in email:
                element = element.lower()
                if (element in unknown_email_chars):
                    valid = False
                    break
            for element in needed_email_chars:
                if (element not in email):
                    valid = False
                    break
            if (valid == False):
                flash(alert_messages['not_valid_email']%(email))
            else:
                status = self.db.add_contact_message(
                    {
                        "vorname": vorname, "nachname": nachname,
                        "telefon": telefon, "anmerkung": anmerkung
                    }
                )
                
                if (status == False):
                    flash(alert_messages['error_while_sending_msg'])
            return redirect(url_for('kontakt_route'))

    def impressum_route(self):
        name = "impressum"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data
        )

    def tortensortiment_route(self):
        name = "tortensortiment"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data,
            tortensortiment = self.db.get_tortensortiment()
        )

    def login_route(self):
        name = "login"
        if (self.db.check_if_logged_in(session) == False):
            if (request.method == "GET"):
                regular_data = self.get_regular_resp_data(name)
                return render_template(
                    regular_data['page_path'],
                    regular_data = regular_data
                )
            else: # Handle Post-Request
                return redirect(url_for('login_route'))
        else:
            return redirect(url_for('dashboard_route'))

    def dashboard_route(self):
        name = "dashboard"
        alert_messages = self.conf.get('Requests','dashboard_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            regular_data = self.get_regular_resp_data(name)
            return render_template(
                regular_data['page_path'],
                regular_data = regular_data,
                username = session['username']
            )
        else:
            flash(alert_messages['need_to_bee_logged_in'])
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
