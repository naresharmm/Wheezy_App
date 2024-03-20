from wheezy.web.handlers import BaseHandler
from main import UserValidator, NodesController, DataController, UserController
from countries import get_countries
from flask import session  

class HomeHandler(BaseHandler):
    def get(self):
        countries = get_countries()
        return self.render_response( 
            'home.html',
            countries=countries
        )


class ProfileHandler(BaseHandler):
    def get(self):
        nodes = UserController().get_profile(session)
        return self.render_response('profile.html', nodes=nodes)


class RegisterFormHandler(BaseHandler):
    def get(self):
        return self.render_response(
            'registration.html',
            countries=get_countries()
        )

class RegisterHandler(BaseHandler):
    def post(self):
        user_validator = UserValidator()
        form_data = self.request.form
        error_message = user_validator.validate_registration(form_data)
        if not error_message:
            return self.redirect_for('profile')
        else:
            return self.render_response(  
                'registration.html',
                countries=get_countries(),
                error_message=error_message
            )

class LoginFormHandler(BaseHandler):
    def get(self):
        return self.render_response('login.html')

class LoginHandler(BaseHandler):
    def post(self):
        if UserController().login(
            self.request.form.get('phone_number'),
            self.request.form.get('password'), session):
            return self.redirect_for('profile')
        else:
            error_message = "The phone number or\
            password is incorrect. Please double-check your credentials"
            return self.render_response(
                'login.html',
                error_message=error_message
            )


class LogoutHandler(BaseHandler):
    def get(self):
        session.clear()
        return self.redirect_for('home')


class SaveTextHandler(BaseHandler):
    def post(self):
        request_data = self.request.get_json()
        response = NodesController().save_text(
            text_data=request_data,
            session=session
        )
        return self.json_response(response)


class DeleteTextHandler(BaseHandler):
    def get(self, node_id):
        response = DataController().delete_text(node_id, session)
        return self.json_response(response)
    

class EditTextHandler(BaseHandler):
    def post(self, node_id):
        response = DataController().edit_text(
            node_id,
            self.request.json.get('new_text'),
            session
        )
        return self.json_response(response)
