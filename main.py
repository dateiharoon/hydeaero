from flask import Flask, render_template, request, redirect, url_for, session,flash
#from forms import LoginForm, RegistrationForm
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager,UserMixin
from flask_login import login_user, logout_user,current_user,login_required
import MySQLdb.cursors
import re
import json
import numpy as np



app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '3.223.61.173'
app.config['MYSQL_USER'] = 'haroon'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'test'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('hydehome.html', username=session['username'])
    # User is not loggedin redirect to login page
# Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM demo2 WHERE username = %s AND password =md5(%s)', (username, password))
        # Fetch one record and return result
        values = cursor.fetchone()
                # If account exists in accounts table in out database
        if values:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = values['id']
            session['username'] = values['username']
            # Redirect to home page
            return render_template('hydehome.html', username=session['username'])
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM demo2 WHERE username = %s", [username])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO demo2 VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

  


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM demo2 WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/supplier.html', methods=["GET", "POST"])
def supplier():
    if 'loggedin' in session:
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute("SELECT * FROM supplierDashbord")
          values = cursor.fetchall()
          print(values)
          print(str(values))
          return render_template('supplier.html', data=values,username=session['username'])
    return redirect(url_for('login'))
       
        
  
@app.route('/fetch')
def fetch():
    ##curs = dbconn.cursor()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM supplierDashbord")
    values = cursor.fetchall()
    #dbconn.close()
    print(values)
    return render_template("fetch.html", result=values)
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Login')


@app.route('/process.html')
def process():
    return render_template('process.html', the_title='Process')


@app.route('/output.html')
def output():
    return render_template('output.html', the_title='Output')

@app.route('/input.html')
def input():
    return render_template('input.html', the_title='Input')



@app.route('/customer.html')
def customer():
    return render_template('customer.html', the_title='Customer')

if __name__ =='__main__':
    app.run(debug=True)