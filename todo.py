from app import app
from user import User
from forms import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, jsonify, request, flash
import pymysql.cursors
import requests
import time

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'no'
login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('todo'))

        flash("incorrect username or password")
        redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/todo/create", methods=["POST"])
def createItem():
    newItem = request.form["InputData"]
    priKey = 0
    if(newItem !=""):
        # conn = pymysql.connect(host = '0.0.0.0',user='username',password='myproject',database='todo')
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO `todolist` (`things`, `user`) VALUES (%s,%s)"
                cursor.execute(sql, (newItem,current_user.username))
                priKey = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()
            return jsonify({"success" : newItem, 'key' : priKey})
    return jsonify({"error" : "no input"})

@app.route("/todo/read")
def getList():
    try:
        # conn = pymysql.connect(host = '0.0.0.0',user='username',password='myproject',database='todo')
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')
        
        with conn.cursor() as cursor:
            sql = "SELECT * FROM todolist Where user=(%s)"
            cursor.execute(sql,(current_user.username))
            result = cursor.fetchall()
    finally:
        conn.close()
        return jsonify(result)

@app.route("/todo/delete", methods=["DELETE"])
def deleteItem():
    Deleted = request.form["data"]
    key = request.form["key"]
    try:
        # conn = pymysql.connect(host = '0.0.0.0',user='username',password='myproject',database='todo')
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')
        
        with conn.cursor() as cursor:
            sql = "DELETE FROM todolist WHERE id=(%s)"
            cursor.execute(sql,(key))
        conn.commit()
    finally:
        conn.close()
        return jsonify({'success' : Deleted})

@app.route("/todo/update", methods=["PUT"])
def updateItem():
    Old = request.form['old']
    New = request.form['item']
    key = request.form['key']
    try:
        # conn = pymysql.connect(host = '0.0.0.0',user='username',password='myproject',database='todo')
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')
        

        with conn.cursor() as cursor:
            sql = "UPDATE todolist SET things =(%s) WHERE id=(%s)"
            cursor.execute(sql,(New, key))
            conn.commit()
    finally:
        conn.close()
        return jsonify({'success' : New})

@app.route("/")
def home():
    if current_user:
        return render_template("home.html", name = current_user.username)
    return render_template("home.html", name = "no")

@app.route('/index/record', methods=['POST'])
def record():
    thing = request.form['thing1']
    year = request.form['year']
    month = request.form['month']
    date = request.form['date']
    print(thing)
    if(thing !=""):
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')  
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO `record` (`username`,`year`,`month`,`date`,`things`) VALUES (%s,%s,%s,%s,%s)" 
                cursor.execute(sql,(current_user.username, year, month, date, thing))
            conn.commit()  
        finally:
            conn.close()
            return jsonify({"well" : thing})
    return jsonify({"error" : "no input"})

@app.route("/index/delete", methods=["DELETE"])
def delete():
    thing = request.form['thing']
    year = request.form['year']
    month = request.form['month']
    date = request.form['date']
    conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM record WHERE username=(%s) AND things=(%s) AND year = (%s) AND month = (%s) AND date =(%s)"
            cursor.execute(sql,(current_user.username, thing, year, month, date))
            # cursor.execute(sql,(current_user.username, year, month, date, thing))
        conn.commit()
    finally:
        conn.close()
        return jsonify({"well" : thing})
    return jsonify({"error" : "sth wrong"})
            

@app.route("/index/read", methods=["POST"])
def getRecords():
    year = request.form['year']
    month = request.form['month']
    date = request.form['date']
    try:
        # conn = pymysql.connect(host = '0.0.0.0',user='username',password='myproject',database='todo')
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')
        
        with conn.cursor() as cursor:
            sql = "SELECT * FROM record Where username=(%s) AND year = (%s) AND month = (%s) AND date =(%s)"
            cursor.execute(sql,(current_user.username,year,month,date))
            result = cursor.fetchall()
    finally:
        conn.close()
        return jsonify(result) 

@app.route("/index/past/readall")
def getAllRecords():
    try:
        # conn = pymysql.connect(host = '0.0.0.0',user='username',password='myproject',database='todo')
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')
        
        with conn.cursor() as cursor:
            sql = "SELECT * FROM record Where username=(%s)"
            cursor.execute(sql,(current_user.username))
            result = cursor.fetchall()
    finally:
        conn.close()
        return jsonify(result) 
@app.route("/index/past")
def past():
    return render_template('allpast.html')

@app.route("/index")
@login_required
def todo():
    res = requests.get("https://ipinfo.io/?token=0392452a65236d")
    data = res.json()
    location = data['loc'].split(',')
    city = data['city']
    lat = location[0]
    lon = location[1]
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid=d4263a7e16cebc434cec16159ba79a56")
    json_object = r.json()
    temp_k = int(json_object['main']['temp'] - 273)
    weather = json_object['weather'][0]['description']

    return render_template("index.html", name = current_user.username, city=city, temp = temp_k, weather=weather)