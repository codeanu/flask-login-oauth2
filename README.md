Flask-Login and Google Oauth2 
=============================

flask-login-oauth2 and google oauth2 library for authenticating new users and maintaining session 

Just register your new Google app at https://code.google.com/apis/console#access 
and register these values:

    CLIENT_ID                in server.py
    CLIENT_SECRET            in server.py
    REDIRECT_URI             in modules/oauth2.py

run the server 
    $python server.py
    Running on http://127.0.0.1:5000/

Register a new user also loggin in if the user exists
http://127.0.0.1:5000/login?email=anurag@grexit.com


To Logout
http://127.0.0.1:5000/logout

Flask-Login Reference
---------------------
http://packages.python.org/Flask-Login/

Google Oauth2 Library Reference
-------------------------------

https://developers.google.com/accounts/docs/OAuth2Login

https://developers.google.com/api-client-library/python/guide/aaa_oauth

