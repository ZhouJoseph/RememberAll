from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql.cursors

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Zhoukx.joseph/Desktop/CS1122/project1-tg1632-zds238-cz1529-kz1005-jjz282/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=45)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route("/")
def home():
	return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('todo'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route("/todo/create", methods=["POST"])
def createItem():
    newItem = request.form["InputData"]
    priKey = 0
    if(newItem !=""):
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
        conn = pymysql.connect(host = 'localhost',user='username',password='cs1122project',database='todo')

        with conn.cursor() as cursor:
            sql = "UPDATE todolist SET things =(%s) WHERE id=(%s)"
            cursor.execute(sql,(New, key))
            conn.commit()
    finally:
        conn.close()
        return jsonify({'success' : New})


@app.route("/index")
@login_required
def todo():
	return render_template("index.html", name = current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
	app.run (debug=True)
