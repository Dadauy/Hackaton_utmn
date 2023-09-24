from app import app

from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, ProjectForm, DeleteProfile, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project
from werkzeug.urls import url_parse
from app import db


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<profile_uuid>/delete', methods=["GET", "POST"])
@login_required
def delete(profile_uuid):
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }

    form = DeleteProfile()
    user = User.query.filter_by(uuid=profile_uuid).first_or_404()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', user=user, data=data, form=form)


@app.route("/profile/<profile_uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(profile_uuid):
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }
    form = EditProfileForm()
    user = User.query.filter_by(uuid=profile_uuid).first_or_404()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.info = form.info.data
        db.session.commit()
        return redirect(url_for('profile', profile_uuid=user.uuid))
    return render_template('edit.html', user=user, data=data, form=form)


@app.route("/profile/<profile_uuid>")
@login_required
def profile(profile_uuid):
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }

    user = User.query.filter_by(uuid=profile_uuid).first_or_404()
    return render_template('profile.html', user=user, data=data)


@app.route("/about")
def about():
    return """Надо реализовать"""


@app.route("/")
def index():
    data = {
        "is_auth": current_user.is_authenticated,
    }
    if data["is_auth"]:
        data["profile_uuid"] = current_user.uuid

    return render_template('index.html', data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    data = {
        "is_auth": current_user.is_authenticated,
    }
    if data["is_auth"]:
        data["profile_uuid"] = current_user.uuid

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
        "is_auth": current_user.is_authenticated,
    }
    if data["is_auth"]:
        data["profile_uuid"] = current_user.uuid

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
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }

    form = ProjectForm()
    if form.validate_on_submit():
        project = Project()
        project.name = form.title.data
        project.city = form.city.data
        project.street = form.street.data
        project.home = form.home.data
        project.text = form.text.data
        project.creator = current_user.id

        user = User.query.filter_by(id=current_user.id).first()
        user.add_projects(project.id)  # projects.id is None - исправить

        db.session.add(project)
        db.session.commit()

        return redirect(url_for('archive'))
    return render_template('create_project.html', form=form, data=data)


@app.route("/archive")
@login_required
def archive():
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }

    return render_template('archive.html', data=data)
