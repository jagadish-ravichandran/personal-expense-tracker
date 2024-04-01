import flask
from flask import make_response, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from config.authentication import SessionUser
from config.constants import ErrorConstants
from config.factory import AppFlask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired

from services.users import UserService


class LoginForm(FlaskForm):
    email = StringField('Email',
                        id='email_login',
                        validators=[DataRequired()])
    password = PasswordField('Password',
                             id='password_login',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='password_create',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')


app = AppFlask().instance


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    template = render_template('register.html', form=form)
    if not form.validate_on_submit():
        return template
    email = form.email.data
    password = form.password.data
    if UserService.is_existed(email):
        flash(ErrorConstants.DUPLICATE_EMAIL_REG, 'error')
        return template
    # resp = make_response(render_template('email_confirmation.html', email=entered_email))
    UserService.register(email, password)
    return make_response(redirect(location=url_for('login')))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    template = render_template('login.html', form=form)

    if not form.validate_on_submit():
        return template

    email = form.email.data
    if not UserService.is_existed(email):
        flash(ErrorConstants.ACCOUNT_NOT_FOUND, "error")
        return template
    password = form.password.data
    if not UserService.validate_password(email, password):
        flash(ErrorConstants.WRONG_PASSWORD, "error")
        return template
    user = UserService.get(email)
    usr_obj = SessionUser(user["id"], user["email"])
    login_user(usr_obj, remember=True)
    redirecting_page = redirect(flask.request.args.get('next') or url_for('dashboard'))
    success_response = make_response(redirecting_page)
    flash("Logged In", "success")
    return success_response


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged Out', 'success')
    return redirect(url_for('login'))
