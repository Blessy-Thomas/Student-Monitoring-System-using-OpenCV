import os
import re

import MySQLdb.cursors
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

from index import d_dtcn

secret_key = str(os.urandom(24))

app = Flask(__name__)
app.config['TESTING'] = True
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = secret_key
app.config['DEBUG'] = True


# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# Defining the home page of our site


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            if (account['ut_id'] == 0):
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                return redirect(url_for('teacher'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('loreg.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('index'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "firstname", "lastname", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'password' in request.form and 'email' in request.form and 'mobile' in request.form and 'ut_id' in request.form:
        # Create variables for easy access
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']
        ut_id = request.form['ut_id']
        mobile = request.form['mobile']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', mobile):
            msg = 'Mobile no. must contain only numbers!'
        elif not username or not firstname or not lastname or not password or not email or not mobile:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s,%s, %s, %s, %s, %s)',
                           (username, firstname, lastname, password, email, ut_id, mobile))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users i.e. students
@app.route('/pythonlogin/home', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/teacher - this will be the teacher home page, only accessible for loggedin users i.e. teacher
@app.route('/pythonlogin/teacher', methods=['GET', 'POST'])
def teacher():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
        'SELECT * FROM accounts WHERE ut_id=1')
        user = cursor.fetchone()
        return render_template('teacher.html', username=session['username'],user=user)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/start- this will be the detection page, to check attentiveness of students
@app.route("/start", methods=['GET', 'POST'])
def start():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Start') == 'Start':
            d_dtcn(session['id'])
            return render_template("home.html")
    else:
        # pass # unknown
        return render_template("index.html")

# http://localhost:5000/pythinlogin/report/<id>- this will be the report/results page, to view their results by students
@app.route("/pythonlogin/reports/<id>", methods=['GET'])
def report(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """SELECT * 
        FROM reports 
        WHERE userid = %s 
        ORDER BY rid DESC LIMIT 0,1""", (id,))
    reports = cursor.fetchall()

    cursor.execute(
        """SELECT a.firstname,a.lastname 
        FROM accounts a,reports r
        WHERE a.id=r.userid AND a.id = %s""", (id,))
    user = cursor.fetchone()

    return render_template("report.html", reports=reports, user=user)

# http://localhost:5000/pythinlogin/teacher/report/- this will be the report/results page, reports of all students will be viewed by the teacher
@app.route("/pythonlogin/teacher/report/", methods=['GET'])
def rep():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """SELECT a.firstname, a.lastname, a.email, a.mobile, r.rid, r.userid, 
            max(r.folder_string) AS folder_string ,max(r.timestamp) AS timestamp 
        FROM reports r, accounts a 
        WHERE a.id= r.userid GROUP BY r.userid""")
    reports = cursor.fetchall()
    return render_template("rep.html", reports=reports)


if __name__ == "__main__":
    app.run()
    app.debug = True
