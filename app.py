from flask import Flask, render_template, redirect, request, url_for,flash, abort
from flask_paginate import Pagination, get_page_parameter
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Flask Forms Imports
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

# Flask SQLAlchemy Imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Flask Login Imports
from flask_login import UserMixin # For DB Models - by inheriting from usermixin, we get access to builtin attributes for views
from flask_login import LoginManager # For Login Management
from flask_login import login_user, logout_user, login_required #2 functions, and 1 decorator (login_required)!!!

# Flask Config
app = Flask(__name__)
app.config['SECRET_KEY']='ASDG'

# Flask SQLAlchemy Config
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
db = SQLAlchemy(app)
Migrate(app,db)

# Flask_Login Config
login_manager = LoginManager()
login_manager.init_app(app) #allows app to now supportlogin
login_manager.login_view = 'login'

# Routes for Data Results (Requires being Logged in before you can click this!)
# @app.route('/results/<site>') #Disabled for now
# def results(site):
    # print('site', site)
@app.route('/results/')
def results():

    # Flask Request Object values
    print('path', request.path)
    print('full_path', request.full_path)
    print('script_root', request.script_root)
    print('base_url', request.base_url)
    print('url', request.url)
    print('url_root', request.url_root)

    # Generate some example results (in this case, just strings from 'A' to 'Z')
    results = list(map(chr, range(ord('A'), ord('Z')+1)))
    
    # Get the page number from the query parameters
    page_number = request.args.get(get_page_parameter(), type=int, default=1)
    
    # Define the number of results per page
    per_page = 5
    
    # Calculate the start and end indexes of the results to be displayed on the current page
    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page
    
    # Create a Pagination object with the total number of results and the number of results per page
    pagination = Pagination(page=page_number, total=len(results), per_page=per_page)
    
    # Pass the results for the current page and the pagination object to the template
    return render_template('results.html', results=results[start_index:end_index], pagination=pagination, page_parameter=get_page_parameter())

#####################
# Routes for Logins #
#####################
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #grab the user based of the email provided by the login

        if user.check_password(form.passw.data) and user is not None:
            # assuming they have password and not logged in
            login_user(user)
            flash('Logged in succefully!')
            # now if the user wanted to visit a page that required a login, we can save that as next
            next = request.args.get('next') 
            if next == None or not next[0]=='/': #check if next exists, otherwise go to welcome page
                next = url_for('welcome_user')
            return redirect(next) #redirect them to the page they wanted to access in the beginning

    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.passw.data)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering!")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

#########
# Forms #
#########
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    passw = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    passw = PasswordField('Password',validators=[DataRequired(),EqualTo('passw_confirm',message='Passwords must match!!!')])
    passw_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register!')
    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message='Your email has been already registered!')
    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(message='Your username has been already registered!')
        
##########
# Models #
##########
# This allow flask_login to load the current user and get their login id! (load a user based of their id!)
# See: https://flask-login.readthedocs.io/en/latest/#configuring-your-application
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin): #Double inherit!!!!!!!!!!!
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True) #dont want 2 users with same email
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    def __init__(self,email,username,password) -> None:
        self.email=email
        self.username=username
        self.password_hash = generate_password_hash(password) #We only want to save the password has of the user's real pw!!!!!!
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
if __name__ == '__main__':
    app.run(debug=True)

