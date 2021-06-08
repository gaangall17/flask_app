from flask import render_template, session, redirect, flash, url_for
from app.forms import LoginForm, SignupForm
from . import jobs
from app.sql_service import get_user, put_user
from app.models import UserModel, UserData
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

#Login existing user
@jobs.route('/new', methods=['GET','POST'])
def newjob():
    pass