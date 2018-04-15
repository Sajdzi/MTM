#Do not touch
#region Do not touch


#This script runs the application using a development server.
#It contains the definition of routes and views for the application.


from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

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

#endregion

@app.route('/')
def home():    
    return render_template("home.html")

#Register Page
#region Register Page
#Formularz rejestracyjny
#Klasa formy z walidacjami zrobiona na bazie WTForms:
class RegisterForm(Form):
    displayname = StringField('Display name', [validators.Length(min=2, max=20)])
    login = StringField('Login', [validators.Length(min=5, max=20)])
    password = PasswordField('Password', [
                           validators.DataRequired(), 
                           validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm password')

#Route do formularza:
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        displayname = form.displayname.data
        login = form.login.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #DB kursor
        cur = mysql.connection.cursor()

        #DB query
        cur.execute("INSERT INTO Users(user_displayname, user_login, user_password) VALUES(%s, %s, %s)"
                    , (displayname, login, password))

        #Wysyłamy dane do DB
        mysql.connection.commit()

        #Zamykam połączenie/strumień danych z DB
        cur.close()

        #redirect(url_for('home'))
    
    return render_template("register.html", form=form)

#endregion

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    app.secret_key = 'secret1234554321'
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
