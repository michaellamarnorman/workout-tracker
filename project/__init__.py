from flask import Flask, render_template, redirect, url_for, request, jsonify, abort, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, login_required, current_user, logout_user
from project.forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
from project.models import WorkoutA, User
login_manager.init_app(app)



def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')

def find_previous_and_current_workout(user_id):
  previous_workout = db.session.query(WorkoutA).filter_by(user_id=user_id).order_by(WorkoutA.entry_id.desc()).first()
  prev_stats = {
    'entry_id': previous_workout.entry_id,
    'workout_start_day': previous_workout.start_time,
    'squat': previous_workout.squat_reps,
    'bench': previous_workout.bench_reps,
    'row': previous_workout.row_reps,
    'press': previous_workout.press_reps,
    'deadlift': previous_workout.deadlift_reps,
    'squat_weight': previous_workout.squat_weight,
    'bench_weight': previous_workout.bench_weight,
    'row_weight': previous_workout.row_weight,
    'press_weight': previous_workout.press_weight,
    'deadlift_weight': previous_workout.deadlift_weight,
    'squat_sets': previous_workout.squat_sets,
    'bench_sets': previous_workout.bench_sets,
    'row_sets': previous_workout.row_sets,
    'press_sets': previous_workout.press_sets,
    'deadlift_sets': previous_workout.deadlift_sets,
    'workout_a_or_b': previous_workout.workout_a_b,
    'workout_complete': previous_workout.workout_complete,
    'workout_number': previous_workout.workout_number
  }
  squat_increase = check_if_set_was_failed(previous_workout.squat_reps.split(','),
                  previous_workout.squat_weight) 
 
  if previous_workout.workout_a_b == 'A':
    try:
      pw = db.session.query(WorkoutA).filter_by(workout_a_b="B", user_id=user_id).order_by(WorkoutA.entry_id.desc()).first()
      press_increase = check_if_set_was_failed(pw.press_reps.split(','), 
                      pw.press_weight)
      deadlift_increase = check_if_set_was_failed(pw.deadlift_reps.split(','), 
                    pw.deadlift_weight)
    except AttributeError:
      # never going to hit this exception since I am creating
      # an initial record for workout B upon registering.  Need
      # to redesign so that record is not created and it pulls 
      # initial weights form a profile/settings table
      press_increase = previous_workout.press_weight
      deadlift_increase = previous_workout.deadlift_weight
    next_workout = {
      'squat_weight': squat_increase,
      'press_weight': press_increase,
      'deadlift_weight': deadlift_increase,
      'bench_weight': previous_workout.bench_weight,
      'row_weight': previous_workout.row_weight,
      'workout_a_or_b': 'B',
      'workout_number': previous_workout.workout_number + 1
    }
  else:
    try:
      pw = db.session.query(WorkoutA).filter_by(workout_a_b="A", user_id=user_id).order_by(WorkoutA.entry_id.desc()).first()
      bench_increase = check_if_set_was_failed(pw.bench_reps.split(','), 
                    pw.bench_weight)
      row_increase = check_if_set_was_failed(pw.row_reps.split(','), 
                  pw.row_weight)
    except AttributeError:
      # need to make a section to provide these values to the database in a 
      # seperate table
      bench_increase = 45
      row_increase = 45
    next_workout = {
      'squat_weight': squat_increase,
      'press_weight': previous_workout.press_weight,
      'deadlift_weight': previous_workout.deadlift_weight,
      'bench_weight': bench_increase,
      'row_weight': row_increase,
      'workout_a_or_b': 'A',
      'workout_number': previous_workout.workout_number + 1
    }
  return prev_stats, next_workout


def check_if_set_was_failed(exercise_set, weight):
  failed = False
  if exercise_set == '' or '' in exercise_set:
    return weight
  for reps in exercise_set:
    if int(reps) < 5:
        failed = True
  if failed:
    return weight
  return weight + 5


@login_manager.user_loader
def load_user(userid):
  return db.session.query(User).filter_by(id=userid).first()




@app.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():

  #if request.method == "POST":
    name = form.username.data
    password = form.password.data
    user = db.session.query(User).filter_by(name=name, password=password).first()
    if user:
      login_user(user)
      return redirect(url_for('user_home', username=user.name, userid=user.id))
    else:
      flash("Username or password was incorrect.")
      return redirect(url_for('login'))
  return render_template('login.html', form=form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))


@app.route('/register', methods=["GET", "POST"])
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
      return redirect(url_for('register'))
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
        return redirect(url_for('login'))

  else:
    #error = flash_errors(form)
    return render_template('register.html', form=form)

  return render_template("register.html", form=form)

@app.route('/', methods=["GET", "POST"])
def index():
  user = current_user
  form = LoginForm()
  rform = RegisterForm()
  if current_user.is_authenticated():
    return redirect(url_for('user_home', username=user.name, userid=user.id))
  return render_template('index.html', form=form, rform=rform)


@app.route('/<username>/<int:userid>/home', methods=["GET", "POST"])
@login_required
def user_home(username, userid):
  previous_stats, next_workout = find_previous_and_current_workout(user_id=userid)
  ongoing_workout = db.session.query(WorkoutA).filter_by(workout_complete=0, user_id=userid).order_by(WorkoutA.entry_id.desc()).first()

  if request.method == 'POST':
    if ongoing_workout:
      return redirect(url_for('workout', entry_id=ongoing_workout.entry_id, username=username, userid=userid, workout=ongoing_workout.workout_a_b))
 
    workout = WorkoutA(
      squat_weight=next_workout['squat_weight'], 
      bench_weight=next_workout['bench_weight'],
      row_weight=next_workout['row_weight'], 
      press_weight=next_workout['press_weight'], 
      deadlift_weight=next_workout['deadlift_weight'],
      workout_a_b=next_workout['workout_a_or_b'],
      workout_number=next_workout['workout_number'],
      user_id=userid)
    db.session.add(workout)
    db.session.commit()
    id = db.session.query(WorkoutA).filter_by(user_id=userid).order_by(WorkoutA.entry_id.desc()).first()
    return redirect(url_for('workout', entry_id=id.entry_id, workout=id.workout_a_b, username=username, userid=userid))

  if ongoing_workout:
    return render_template('user_home.html', prev_stats=previous_stats, ongoing_workout=ongoing_workout)

  return render_template('user_home.html', prev_stats = previous_stats, next_stats=next_workout)


@app.route('/<username>/<int:userid>/workout/<int:entry_id>/<workout>')
def workout(entry_id, workout, username, userid):
  continued = WorkoutA.query.filter_by(entry_id=entry_id, user_id=userid).first()
  if continued:
    return render_template('workout.html', id=entry_id, workout=workout, workout_stats=continued, username=username, userid=userid)
  
    # Belowis not used.  need to add try, except to catch
    # when a user tries to go directly to a url where,
    # the workout does not exist. 
  workout_stats = WorkoutA.query.filter_by(entry_id=entry_id, user_id=userid).first()
  return render_template('workout.html', id=entry_id, workout=workout, workout_stats=workout_stats, username=username, userid=userid)


@app.route('/save_workout/<username>/<int:userid>/<int:entry_id>', methods=['GET', "POST"])
def save_workout(entry_id, username, userid):

    if request.method == "POST":
      #complete_flag = 1
      squat_reps = request.form.get('squat')
      workout_complete = WorkoutA.query.filter_by(entry_id=entry_id, user_id=userid).first()
      if workout_complete.workout_a_b == "A":
        bench_reps = request.form.get('bench')
        row_reps = request.form.get('row')

        if squat_reps and bench_reps and row_reps:
          workout_complete.squat_reps = squat_reps
          workout_complete.bench_reps = bench_reps
          workout_complete.row_reps = row_reps
          workout_complete.workout_complete = 1
          db.session.commit()

      if workout_complete.workout_a_b == "B":
        press_reps = request.form.get('press')
        deadlift_reps = request.form.get('deadlift')
        if deadlift_reps == '':
          deadlift_reps = ','
        

        if squat_reps and press_reps:
          workout_complete.squat_reps = squat_reps
          workout_complete.press_reps = press_reps
          workout_complete.deadlift_reps = deadlift_reps
          workout_complete.workout_complete = 1
          db.session.commit()
      flash("Workout saved successfully!")  
      return redirect(url_for('user_home', username=username, userid=userid))


@app.route('/database-view/<username>/<int:userid>')
def database_view(username, userid):
  workouts = db.session.query(WorkoutA).filter_by(user_id=userid).order_by(WorkoutA.entry_id.desc())
  return render_template('database-view.html', workouts=workouts)


@app.route('/write_updates/<username>/<int:userid>/<int:entry_id>', methods=["GET", "POST"])
def write_set_change(entry_id, username, userid):
    if request.method == "POST":
    #complete_flag = 1
      squat_reps = request.form.get('squat')
      workout_complete = WorkoutA.query.filter_by(entry_id=entry_id, user_id=userid).first()
      if workout_complete.workout_a_b == "A":
        bench_reps = request.form.get('bench')
        row_reps = request.form.get('row')

        if squat_reps and bench_reps and row_reps:
          workout_complete.squat_reps = squat_reps
          workout_complete.bench_reps = bench_reps
          workout_complete.row_reps = row_reps
          db.session.commit()
          return "workout A success"
        else: 
          "there was an error saving your workout"

      if workout_complete.workout_a_b == "B":
        press_reps = request.form.get('press')
        deadlift_reps = request.form.get('deadlift')
        if deadlift_reps == '':
          deadlift_reps = ','
        

        if squat_reps and press_reps:
          workout_complete.squat_reps = squat_reps
          workout_complete.press_reps = press_reps
          workout_complete.deadlift_reps = deadlift_reps
          db.session.commit()
          return "Workout B saved"
        else:
          "there was an error saving your workout"
