from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('User', validators=[
        DataRequired(),
        Length(min=4, max=12)
    ])
    email = StringField('Email Address', validators=[
        DataRequired(),
        Length(min=6, max=50)
    ])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Submit Request')

class AssetForm(FlaskForm):
    vfp_id = StringField('VFD ID')
    name = StringField('Nombre', default='Asset de Prueba')
    submit = SubmitField('Guardar')

class UserProfileForm(FlaskForm):
    username = StringField('Username', render_kw={'readonly': True})
    name = StringField('Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    phone = StringField('Phone')
    role = StringField('Role', render_kw={'readonly': True})
    status = SelectField('Status', coerce=int, validators=[DataRequired()])
#     status = QuerySelectField(query_factory=Area.objects.all,
# #                            get_pk=lambda a: a.id,
# #                            get_label=lambda a: a.name)
    submit = SubmitField('Actualizar')