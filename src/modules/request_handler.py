"""
Bäckerei Neumeyer/Request Handler/Python 3.8.10
"""
import sys,os
from flask import (render_template, redirect, send_from_directory, request, url_for, session, flash)
sys.dont_write_bytecode = True
from datetime import datetime

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
        data['logged_in_status'] = self.db.check_if_logged_in(session)
        data['page_name'] = page_name
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

    def pages_editor_route(self):
        name = "pages_editor"
        regular_data = self.get_regular_resp_data(name)
        if (regular_data['logged_in_status'] == True):
            return render_template(
                regular_data['page_path'],
                regular_data = regular_data,
                tortensortiment_len = self.db.get_number_of_tortensortiment(),
                tortensortiment = self.db.get_tortensortiment(),
                hochzeitstorten_len = self.db.get_number_of_hochzeitstorten(),
                hochzeitstorten = self.db.get_hochzeitstorten()
            )
        else:
            alert_messages = self.conf.get('Requests','pages_editor_route')['alert_messages']
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def tortensortiment_remove_route(self):
        alert_messages = self.conf.get('Requests','tortensortiment_remove_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            torten_name = request.form.get('torten_name')
            status = self.db.tortensortiment_remove_one(torten_name)
            if (status == True):
                pass
            else:
                flash(alert_messages['could_not_remove_torte']%(torten_name))
            return redirect(url_for('tortensortiment_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def tortensortiment_add_route(self):
        alert_messages = self.conf.get('Requests','tortensortiment_add_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            torten_name = request.form.get('torten_name')
            torten_img = request.files['torten_img']
            torten_description = request.form.get('torten_description')
            upload_path = self.conf.get('Webserver','img_upload_folder')
            now = datetime.now()
            upload_zeitpunkt = f"{now.day}.{now.month}.{now.year}"
            dateiname = torten_img.filename
            path = os.path.join(upload_path, dateiname)
            db_torten_img_path = url_for('img_route',path="uploaded/"+dateiname)
            torten_img.save(path)
            if (".jpg" in dateiname or ".png" in dateiname or ".jpeg" in dateiname):
                self.db.tortensortiment_add_one([torten_name,db_torten_img_path,torten_description,upload_zeitpunkt])
            else:
                flash(alert_messages['not_a_valid_img_file'])
            return redirect(url_for('pages_editor_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def edit_tortensortiment_route(self):
        alert_messages = self.conf.get('Requests','edit_tortensortiment_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            old_torten_name = request.form.get('old_torten_name')
            new_torten_name = request.form.get('new_torten_name')
            torten_name = new_torten_name
            if (new_torten_name == "" or new_torten_name == " "):
                torten_name = old_torten_name
            (status,data) = self.db.get_one_tortensortiment(old_torten_name)
            if (status == True):
                torten_img = request.files['torten_img']
                torten_description = request.form.get('torten_description')
                if (torten_description == "" or torten_description == data['torten_description']):
                    torten_description = data['torten_description']
                upload_path = self.conf.get('Webserver','img_upload_folder')
                now = datetime.now()
                upload_zeitpunkt = f"{now.day}.{now.month}.{now.year}"
                dateiname = torten_img.filename
                if (dateiname in data['torten_img_path'] or dateiname == "" or dateiname == " "):
                    db_torten_img_path = data['torten_img_path']
                else:
                    path = os.path.join(upload_path, dateiname)
                    db_torten_img_path = url_for('img_route',path="uploaded/"+dateiname)
                    torten_img.save(path)
                print(db_torten_img_path)
                if (".jpg" in db_torten_img_path or ".png" in db_torten_img_path or ".jpeg" in db_torten_img_path):
                    status = self.db.update_tortensortiment([old_torten_name,torten_name,db_torten_img_path,torten_description,upload_zeitpunkt])
                    if (status == False):
                        flash(alert_messages['failed_to_update'])
                    else:
                        flash(alert_messages['updated_torte']%(torten_name))
                else:
                    flash(alert_messages['not_a_valid_img_file'])
                return redirect(url_for('tortensortiment_route'))
            else:
                flash(alert_messages['torte_does_not_exist']%(old_torten_name))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def edit_hochzeitstorte_route(self):
        alert_messages = self.conf.get('Requests','edit_hochzeitstorte_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            old_torten_name = request.form.get('old_torten_name')
            new_torten_name = request.form.get('new_torten_name')
            torten_name = new_torten_name
            if (new_torten_name == "" or new_torten_name == " "):
                torten_name = old_torten_name
            (status,data) = self.db.get_one_hochzeitstorte(old_torten_name)
            if (status == True):
                torten_img = request.files['torten_img']
                torten_description = request.form.get('torten_description')
                if (torten_description == "" or torten_description == data['torten_description']):
                    torten_description = data['torten_description']
                upload_path = self.conf.get('Webserver','img_upload_folder')
                now = datetime.now()
                upload_zeitpunkt = f"{now.day}.{now.month}.{now.year}"
                dateiname = torten_img.filename
                if (dateiname in data['torten_img_path'] or dateiname == "" or dateiname == " "):
                    db_torten_img_path = data['torten_img_path']
                else:
                    path = os.path.join(upload_path, dateiname)
                    db_torten_img_path = url_for('img_route',path="uploaded/"+dateiname)
                    torten_img.save(path)
                print(db_torten_img_path)
                if (".jpg" in db_torten_img_path or ".png" in db_torten_img_path or ".jpeg" in db_torten_img_path):
                    status = self.db.update_hochzeitstorte([old_torten_name,torten_name,db_torten_img_path,torten_description,upload_zeitpunkt])
                    if (status == False):
                        flash(alert_messages['failed_to_update'])
                    else:
                        flash(alert_messages['updated_torte']%(torten_name))
                else:
                    flash(alert_messages['not_a_valid_img_file'])
                return redirect(url_for('hochzeitstorten_route'))
            else:
                flash(alert_messages['torte_does_not_exist']%(old_torten_name))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

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

    def team_route(self):
        name = "team"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data,
            team = self.db.get_team()
        )

    def logout_all_devices_route(self):
        alert_messages = self.conf.get('Requests','logout_all_devices_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            self.db.logout_all_devices(session)
            return redirect(url_for('logout_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def logout_other_device_route(self,session_id):
        alert_messages = self.conf.get('Requests','logout_other_device_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            self.db.delete_other_device(session_id)
            flash(alert_messages['logged_out_another_device']%(session_id))
            return redirect(url_for('dashboard_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def delete_contact_msg_route(self,msg_id):
        alert_messages = self.conf.get('Requests','delete_contact_msg_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            status = self.db.delete_contact_message(msg_id)
            if (status == True):
                flash(alert_messages['deleted_contact_msg']%(msg_id))
            else:
                flash(alert_messages['not_valid_msg_id']%(msg_id))
            return redirect(url_for('dashboard_route'))
        else:
            flash(alert_messages['need_to_be_logged_in'])
            return redirect(url_for('login_route'))
    
    def remove_team_member_route(self):
        alert_messages = self.conf.get('Requests','remove_team_member_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            vorname = request.form.get('vorname')
            nachname = request.form.get('nachname')
            status = self.db.delete_team_member(vorname,nachname)
            if (status == False):
                flash(alert_messages['not_valid_member_name'])
            else:
                flash(alert_messages['removed_team_member']%(vorname,nachname))
            return redirect(url_for('team_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def hochzeitstorten_route(self):
        name = "hochzeitstorten"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data,
            hochzeitstorten = self.db.get_hochzeitstorten()
        )

    def remove_hochzeitstorte_route(self):
        alert_messages = self.conf.get('Requests','remove_hochzeitstorte_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            torten_name = request.form.get('torten_name')
            status = self.db.remove_hochzeitstorte(torten_name)
            if (status == True):
                pass
            else:
                flash(alert_messages['could_not_remove_torte']%(torten_name))
            return redirect(url_for('hochzeitstorten_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

    def add_hochzeitstorte_route(self):
        alert_messages = self.conf.get('Requests','add_hochzeitstorte_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            torten_name = request.form.get('torten_name')
            torten_img = request.files['torten_img']
            torten_description = request.form.get('torten_description')
            upload_path = self.conf.get('Webserver','img_upload_folder')
            now = datetime.now()
            upload_zeitpunkt = f"{now.day}.{now.month}.{now.year}"
            dateiname = torten_img.filename
            path = os.path.join(upload_path, dateiname)
            db_torten_img_path = url_for('img_route',path="uploaded/"+dateiname)
            torten_img.save(path)
            if (".jpg" in dateiname or ".png" in dateiname or ".jpeg" in dateiname):
                self.db.add_hochzeitstorte([torten_name,db_torten_img_path,torten_description,upload_zeitpunkt])
            else:
                flash(alert_messages['not_a_valid_img_file'])
            return redirect(url_for('hochzeitstorten_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))
    
    def add_team_member_route(self):
        alert_messages = self.conf.get('Requests','add_team_member_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            vorname = request.form.get('vorname')
            nachname = request.form.get('nachname')
            arbeitsplatz = request.form.get('arbeitsplatz')
            member_img = request.files['member_img']
            upload_path = self.conf.get('Webserver','img_upload_folder')
            dateiname = member_img.filename
            path = os.path.join(upload_path, dateiname)
            img_path = url_for('img_route', path="uploaded/"+dateiname)
            member_img.save(path)
            if (".jpg" in dateiname or ".png" in dateiname or ".jpeg" in dateiname):
                self.db.add_team_member([vorname,nachname,arbeitsplatz,img_path])
                flash(alert_messages['added_team_member']%(vorname,nachname))
            else:
                flash(alert_messages['not_a_valid_img_file'])
            return redirect(url_for('dashboard_route'))
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))

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
                        "email": email, "telefon": telefon, "anmerkung": anmerkung
                    }
                )
                
                if (status == False):
                    flash(alert_messages['error_while_sending_msg'])
                else:
                    flash(alert_messages['sent_msg'])
            return redirect(url_for('kontakt_route'))

    def impressum_route(self):
        name = "impressum"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data
        )

    def before_request_func(self):
        pass

    def tortensortiment_route(self):
        name = "tortensortiment"
        regular_data = self.get_regular_resp_data(name)
        return render_template(
            regular_data['page_path'],
            regular_data = regular_data,
            tortensortiment = self.db.get_tortensortiment()
        )

    def logout_route(self):
        alert_messages = self.conf.get('Requests','logout_route')['alert_messages']
        if (self.db.check_if_logged_in(session) == True):
            self.db.delete_logged_in_devices(session)
            session.clear()
            flash(alert_messages['logged_out'])
        else:
            flash(alert_messages['need_to_bee_logged_in'])
            return redirect(url_for('login_route'))
        return redirect(url_for('index_route'))

    def login_route(self):
        name = "login"
        alert_messages = self.conf.get('Requests','login_route')['alert_messages']
        regular_data = self.get_regular_resp_data(name)
        if (regular_data['logged_in_status'] == False):
            if (request.method == "GET"):
                return render_template(
                    regular_data['page_path'],
                    regular_data = regular_data
                )
            else: # Handle Post-Request
                username = request.form.get('username')
                password = request.form.get('password')
                (status,new_session_data) = self.db.check_login_data({"username":username,"password":password})
                if (status == False):
                    flash(alert_messages['invalid_login_data'])
                    return redirect(url_for('login_route'))
                else:
                    for element in new_session_data:
                        session[element] = new_session_data[element]
                    flash(alert_messages['logged_in'])
                    return redirect(url_for('dashboard_route'))
        else:
            return redirect(url_for('dashboard_route'))

    def dashboard_route(self):
        name = "dashboard"
        alert_messages = self.conf.get('Requests','dashboard_route')['alert_messages']
        regular_data = self.get_regular_resp_data(name)
        if (regular_data['logged_in_status'] == True):
            return render_template(
                regular_data['page_path'],
                regular_data = regular_data,
                session_data = session,
                number_of_sessions = self.db.get_number_of_sessions(),
                number_of_users = self.db.get_number_of_users(),
                open_sessions = self.db.get_open_sessions(),
                anmerkungen=self.db.get_anmerkungen(),
                number_of_anmerkungen = self.db.get_number_of_anmerkungen(),
                number_of_tortensortiment = self.db.get_number_of_tortensortiment(),
                number_of_team = self.db.get_number_of_team()
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
