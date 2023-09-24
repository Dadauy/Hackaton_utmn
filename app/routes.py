from app import app
import json
from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, ProjectForm, DeleteProfile, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project
from werkzeug.urls import url_parse
from app import db


@app.route("/")
def index():
    data = {
        "is_auth": current_user.is_authenticated,
    }
    if data["is_auth"]:
        data["profile_uuid"] = current_user.uuid

    return render_template('index.html', data=data)


@app.route('/project/<int:project_id>')
def project(project_id):
    data = {
        "is_auth": current_user.is_authenticated,
        "project": Project.query.get(project_id)
    }
    if data["is_auth"]:
        data["profile_uuid"] = current_user.uuid
    return render_template("project.html", data=data)


@app.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }
    projects_ids = json.loads(current_user.created_projects)
    if not(project_id in projects_ids):
        return redirect(url_for("project", project_id=project_id))
    form = EditProjectForm()  # TODO: сделать форму редактирования проекта
    project = Project.query.get_or_404(project_id)
    if form.validate_on_submit():
        project.name = form.name.data
        # ...
        db.session.commit()
        return redirect(url_for('project', project_id=project_id))
    return render_template('edit_project.html', data=data, form=form)


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


@app.route("/my_projects")
@login_required
def my_projects():
    projects = []
    projects_ids = json.loads(current_user.created_projects)
    for pj in Project.query.all():
        if pj.id in projects_ids:
            projects.append(pj)
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid,
        "projects": projects,
    }
    return render_template('my_projects.html', data=data)


@app.route('/create_project', methods=['POST', 'GET'])
@login_required
def create_project():
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid,
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
        db.session.add(project)
        db.session.commit()
        user = User.query.filter_by(id=current_user.id).first()
        project_id = Project.query.filter_by(text=project.text).first().id
        user.add_projects(project_id)  # projects.id is None - исправить
        db.session.commit()
        return redirect(url_for('project', project_id=project_id))
    return render_template('create_project.html', form=form, data=data)


@app.route("/all_projects")
def all_projects():
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid,
        "projects": Project.query.order_by(Project.id.desc()).all(),
    }
    return render_template('all_projects.html', data=data)


@app.route('/profile/<profile_uuid>/delete', methods=["GET", "POST"])
@login_required
def delete(profile_uuid):
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }
    if current_user.uuid != profile_uuid:
        return redirect(url_for("profile", profile_uuid=profile_uuid))
    form = DeleteProfile()
    user = User.query.filter_by(uuid=profile_uuid).first_or_404()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('profile', profile_uuid=profile_uuid))
    return render_template('delete.html', user=user, data=data, form=form)


@app.route("/profile/<profile_uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(profile_uuid):
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid
    }
    if current_user.uuid != profile_uuid:
        return redirect(url_for("profile", profile_uuid=profile_uuid))
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
def profile(profile_uuid):
    data = {
        "is_auth": current_user.is_authenticated,
        "profile_uuid": current_user.uuid if current_user.is_authenticated else None
    }
    user = User.query.filter_by(uuid=profile_uuid).first_or_404()
    return render_template('profile.html', user=user, data=data)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def error_404(e):
    data = {
        "is_auth": current_user.is_authenticated,
        'error': 'Упс. Страница не найдена :('
    }
    return render_template('errors.html', data=data)
