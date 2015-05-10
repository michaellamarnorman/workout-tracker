from flask import Flask, render_template, redirect, url_for, request, jsonify, abort, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, login_required, current_user, logout_user
from project.forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
from project.models import WorkoutA, User


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



from project.users.views import users
from project.profile.views import profile_blueprint
from project.workout.views import workout_blueprint

app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(profile_blueprint, url_prefix='/profile')
app.register_blueprint(workout_blueprint, url_prefix='/workout')

login_manager.login_view = 'users.login'




@app.route('/', methods=["GET", "POST"])
def index():
  user = current_user
  form = LoginForm()
  rform = RegisterForm()
  if current_user.is_authenticated():
    return redirect(url_for('profile.user_home', username=user.name, userid=user.id))
  return render_template('index.html', form=form, rform=rform)


@app.route('/database-view/<username>/<int:userid>')
def database_view(username, userid):
  workouts = db.session.query(WorkoutA).filter_by(user_id=userid).order_by(WorkoutA.entry_id.desc())
  return render_template('database-view.html', workouts=workouts)

