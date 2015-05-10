from flask import Blueprint, render_template, redirect, url_for, flash
from project import db, app, login_manager, load_user
from project.models import User, WorkoutA
from .forms import LoginForm, RegisterForm
from flask.ext.login import login_required, login_user, logout_user

users = Blueprint('user', __name__, 
    template_folder='templates',
    static_folder='static',
    url_prefix='/users')

@users.route('/register', methods=["GET", "POST"])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
  #if request.method == "POST":
    username = form.username.data
    password = form.password.data
    email = form.email.data
    confirm_password = form.confirm.data

    user_name = db.session.query(User).filter_by(name=username).first()
    user_email = db.session.query(User).filter_by(email=email).first()
    if user_name or user_email:
      flash("Username and/or email already exists.")
      return redirect(url_for('user.register'))
    else:
        user = User(
          name=username,
          password=password,
          email=email,
          role='user'
          )
        db.session.add(user)
        db.session.commit()
        new_user = db.session.query(User).filter_by(name=username, email=email).first()
        db.session.add(WorkoutA( 
          workout_complete=1, user_id=new_user.id))
        db.session.commit()
        flash("Registration successfull!")
        return redirect(url_for('user.login'))

  else:
    #error = flash_errors(form)
    return render_template('/users/register.html', form=form)

  return render_template("/users/register.html", form=form)

@users.route('/login', methods=["GET", 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():

  # if request.method == "POST":
    name = form.username.data
    password = form.password.data
    user = db.session.query(User).filter_by(name=name, password=password).first()
    if user:
      login_user(user)
      return redirect(url_for('profile.user_home', username=user.name, userid=user.id))
    else:
      flash("Username or password was incorrect.")
      return redirect(url_for('user.login'))
  return render_template('users/login.html', form=form)


@users.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))


