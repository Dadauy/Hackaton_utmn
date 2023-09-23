from app import app

from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, ProjectForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile")
@login_required
def profile():
    # user = User.query.filter_by(uuid=profile_uuid).first_or_404()
    # return render_template('profile.html', user=user, profile_uuid=profile_uuid)
    return """Надо реализовать"""


@app.route("/archive")
@login_required
def archive():
    return """Надо реализовать"""


@app.route("/about")
def about():
    return """Надо реализовать"""


@app.route("/")
def index():
    data = {
        "is_auth": current_user.is_authenticated
    }

    return render_template('index.html', data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    data = {
        "is_auth": current_user.is_authenticated
    }

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form, data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    data = {
        "is_auth": current_user.is_authenticated
    }

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form, data=data)


@app.route('/create_project', methods=['POST', 'GET'])
@login_required
def create_project():
    data = {
        "is_auth": current_user.is_authenticated
    }

    form = ProjectForm()
    if form.validate_on_submit():
        '''project = Project()
        project.title = form.title.data
        project.text = form.text.data
        db.session.add(project)
        db.session.commit()'''
        return redirect(url_for('index'))
    return render_template('create_project.html', form=form, data=data)
