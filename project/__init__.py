from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from project.models import WorkoutA 


def find_previous_and_current_workout():
  previous_workout = db.session.query(WorkoutA).order_by(WorkoutA.entry_id.desc()).first()
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
    'workout_complete': previous_workout.workout_complete
  }
  squat_increase = check_if_set_was_failed(previous_workout.squat_reps.split(','),
                  previous_workout.squat_weight) 
 
  if previous_workout.workout_a_b == 'A':
    try:
      pw = db.session.query(WorkoutA).filter_by(workout_a_b="B").order_by(WorkoutA.entry_id.desc()).first()
      press_increase = check_if_set_was_failed(pw.press_reps.split(','), 
                      pw.press_weight)
      deadlift_increase = check_if_set_was_failed(pw.deadlift_reps.split(','), 
                    pw.deadlift_weight)
    except AttributeError:
      press_increase = previous_workout.press_weight
      deadlift_increase = previous_workout.deadlift_weight
    next_workout = {
      'squat_weight': squat_increase,
      'press_weight': press_increase,
      'deadlift_weight': deadlift_increase,
      'bench_weight': previous_workout.bench_weight,
      'row_weight': previous_workout.row_weight,
      'workout_a_or_b': 'B'
    }
  else:
    try:
      pw = db.session.query(WorkoutA).filter_by(workout_a_b="A").order_by(WorkoutA.entry_id.desc()).first()
      bench_increase = check_if_set_was_failed(pw.bench_reps.split(','), 
                    pw.bench_weight)
      row_increase = check_if_set_was_failed(pw.row_reps.split(','), 
                  pw.row_weight)
    except AttributeError:
      # need to make a section to provide these values to the database in a 
      # seperate table
      bench_increase = 135
      row_increase = 100
    next_workout = {
      'squat_weight': squat_increase,
      'press_weight': previous_workout.press_weight,
      'deadlift_weight': previous_workout.deadlift_weight,
      'bench_weight': bench_increase,
      'row_weight': row_increase,
      'workout_a_or_b': 'A'
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


@app.route('/', methods=["GET", "POST"])
def index():
  previous_stats, next_workout = find_previous_and_current_workout()


  if request.method == 'POST':
    workout = WorkoutA(
      squat_weight=next_workout['squat_weight'], 
      bench_weight=next_workout['bench_weight'],
      row_weight=next_workout['row_weight'], 
      press_weight=next_workout['press_weight'], 
      deadlift_weight=next_workout['deadlift_weight'],
      workout_a_b=next_workout['workout_a_or_b'])
    db.session.add(workout)
    db.session.commit()
    id = db.session.query(WorkoutA).order_by(WorkoutA.entry_id.desc()).first()
    return redirect(url_for('workout', entry_id=id.entry_id, workout=id.workout_a_b))

  return render_template('index.html', prev_stats = previous_stats, next_stats=next_workout)


@app.route('/workout/<int:entry_id>/<workout>')
def workout(entry_id, workout):
  workout_stats = WorkoutA.query.filter_by(entry_id=entry_id).first()
  return render_template('workout.html', id=entry_id, workout=workout, workout_stats=workout_stats)


@app.route('/save_workout/<int:entry_id>', methods=['GET', "POST"])
def save_workout(entry_id):

    json_results = []
    if request.method == "POST":
      complete_flag = 1
      squat_reps = request.form.get('squat')
      workout_complete = WorkoutA.query.filter_by(entry_id=entry_id).first()
      if workout_complete.workout_a_b == "A":
        bench_reps = request.form.get('bench')
        row_reps = request.form.get('row')

        complete_flag = int('' not in squat_reps.split(',') or
                            '' not in bench_reps.split(',') or
                            '' not in row_reps.split(','))

        if squat_reps and bench_reps and row_reps:
          workout_complete.squat_reps = squat_reps
          workout_complete.bench_reps = bench_reps
          workout_complete.row_reps = row_reps
          workout_complete.workout_complete = complete_flag
          db.session.commit()
          return "workout A success"
        else: 
          return "error"

      if workout_complete.workout_a_b == "B":
        press_reps = request.form.get('press')
        deadlift_reps = request.form.get('deadlift')
        if deadlift_reps == '':
          deadlift_reps = ','
        try:
          complete_flag = int('' not in squat_reps.split(',') or
                              '' not in press_reps.split(',') or 
                              '' not in deadlift_reps.split(',')
                            )
        except Exception:
          return str(Exception)

        if squat_reps and press_reps:
          workout_complete.squat_reps = squat_reps
          workout_complete.press_reps = press_reps
          workout_complete.deadlift_reps = deadlift_reps
          workout_complete.workout_complete = complete_flag
          db.session.commit()
          return "Workout B success"
        else: 
          return "error"


@app.route('/database-view')
def database_view():
  workouts = db.session.query(WorkoutA).order_by(WorkoutA.entry_id.desc())
  return render_template('database-view.html', workouts=workouts)