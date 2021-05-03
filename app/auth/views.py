from flask import render_template, session, redirect, flash, url_for
from app.forms import LoginForm
from . import auth
from app.sql_service import get_user
from app.models import UserModel, UserData
from flask_login import login_user, login_required, logout_user

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
            if password_from_db == password:
                user_data = UserData(username, password)
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

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada')
    return redirect(url_for('auth.login'))