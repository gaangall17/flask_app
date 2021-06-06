from flask import render_template, session, redirect, flash, url_for
from app.forms import LoginForm, SignupForm
from . import auth
from app.sql_service import get_user, put_user
from app.models import UserModel, UserData
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

#Login existing user
@auth.route('/login', methods=['GET','POST'])
def login():

    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():   #Como un Post
         
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)

        if user_doc is not None:
            password_from_db = user_doc.password
            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password, user_doc.email)
                user = UserModel(user_data)

                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('La informacion no coincide')
        else:
            flash('Usuario no existe')



        session['username'] = username

        #flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('login.html', **context)


#Sign up new user
@auth.route('signup', methods=['GET','POST'])
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        email = signup_form.email.data

        user_doc = get_user(username)

        if user_doc is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash, email)

            put_user(user_data)
            flash('Usuario Registrado')

            user = UserModel(user_data)
            login_user(user)

            return redirect(url_for('index'))

        else:
            flash('Usuario ya existe')


    return render_template('signup.html', **context)

#Logout current user
@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada')
    return redirect(url_for('auth.login'))