"""
    INSTALL 
        Flask
        Flask-Login 
        requests 
"""
from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUser,
                             confirm_login, fresh_login_required)
from flask import request
import json
import traceback
import time
import requests
"""
    Imports End 
"""
app = Flask(__name__)
CLIENT_ID = ""
CLIENT_SECRET = ""

""" 
User Session management Class
"""
class User(UserMixin):
    def __init__(self, email, id,fname="", lname="", active=True):
        self.email = email  
        self.id = id
        self.active = active
        self.fname = fname
        self.lname = lname

    def is_active(self):
        return self.active
    def myemail(self):
        return self.email
    def get_userid(self):
        return self.id
    def get_fname(self):
        return self.fname
    def get_lname(self):
        return self.lname

"""
USER_STORE is the store of all the users. Ideally it should be in Database 
"""
USERS = {
    1: User("anurag@grexit.com", 1, "Anurag", "Maher", True)
}

"""
USER_NAMES maintains a dictionary of all the users with their email address 
"""
USER_NAMES = dict((u.email, u) for u in USERS.itervalues())

class Anonymous(AnonymousUser):
    name = u"Anonymous"

@app.route("/")
def hello():
    if current_user.is_authenticated():
        return " User " + str(current_user.myemail()) + " is logged in " 

    return "Hello World!"

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    from modules.oauth2 import GeneratePermissionUrl 
    if current_user.is_authenticated():
        return current_user.get_id()

    if request.method == "GET":
        useremail = request.args.get('email', '')
        if useremail:
            if useremail in USER_NAMES:
                loginit = login_user(USER_NAMES[useremail], remember="yes")
                return "user already exists and logged in"

    if request.method == "GET" and request.args.get('email', ''):
        url = GeneratePermissionUrl(__CLIENT_ID__, request.args.get('email', ''))
        return redirect(url)
    return "No Email Provided"

@app.route("/oauth2callback", methods=["GET", "POST"])
def oauth2callback():
    from grexit.modules.imap.oauth2 import AuthorizeTokens 
    if request.method == "GET":
        authorizationcode = request.args.get('code', '')
        useremail = request.args.get('state', '') 
        response = AuthorizeTokens(CLIENT_ID, 
                                   CLIENT_SECRET, 
                                   authorizationcode) 
        accesstoken = response["access_token"]
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + accesstoken)
        j = json.loads(r.text)
        if useremail != j["email"]:
            return "Initiated e-mail does not match with the authenticated email"
        options = {}
        options["email"] = j.get("email")
        options["firstname"] = j.get("given_name")
        options["lastname"] = j.get("family_name")
        options["accesstoken"] = accesstoken
        u = User(options.get("email"), userid, options.get("firstname"), options.get("lastname"))
        USERS[userid] = u
        loginit = login_user(u, remember="yes")
        if loginit == True:
            return "Everything happened Successfullly"
        return "Some Problem happened"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
app.secret_key = "enter some key" # required for session management in flask

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

if __name__ == "__main__":
    app.run(debug=True)

