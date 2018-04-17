"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import os

app = Flask(__name__)

#inicjalizacja MySQL
mysql = MySQL(app)
#Konfiguracja DB
app.config['MYSQL_HOST'] = 'skupa.atthost24.pl'
app.config['MYSQL_USER'] = '4173_Kajak'
app.config['MYSQL_PASSWORD'] = 'czatkajak1'
app.config['MYSQL_DB'] = '4173_Kajak'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

if __name__ == 'main':
    app.run()
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def home():    
    return render_template("home.html")

@app.route('/register')
def render_register():
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()
    
    if request.method == "POST":
        
        # two methods to ensure that password and username are submited if it will be dealt on frontend then skip it
        # assuming that form fields got "username" and "password" name html atribute
        # if not request.form.get("user_displayname"):
        #     return render_template("error.html")
        # if not request.form.get("user_password"):
        #     return render_template("error.html")
        
        #hardcoding username for testing    
        # user_displayname = request.form.get("user_displayname")
        user_displayname = "Uku"
        password = request.form.get("user_passwordpassword")
        
        #DB kursor
        cur = mysql.connection.cursor()
        
        #DB query
        login_data = cur.execute("SELECT * FROM Users WHERE user_displayname = :user_displayname", username=user_displayname)
        
        print (login_data)
        
    else:
        render_template("login.html")
    
    
    






app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
