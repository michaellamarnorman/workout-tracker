from flask import Blueprint, url_for, redirect, render_template, flash, request
from project import db
from project.models import User, WorkoutA
from flask.ext.login import login_required

workout_blueprint = Blueprint(
    'workout',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix="/workout",
    )



@workout_blueprint.route('/<username>/<int:userid>/workout/<int:entry_id>/<workout>')
def workout(entry_id, workout, username, userid):
  continued = WorkoutA.query.filter_by(entry_id=entry_id, user_id=userid).first()
  if continued:
    return render_template('/workout/workout.html', id=entry_id, workout=workout, workout_stats=continued, username=username, userid=userid)
  
    # Belowis not used.  need to add try, except to catch
    # when a user tries to go directly to a url where,
    # the workout does not exist. 
  workout_stats = WorkoutA.query.filter_by(entry_id=entry_id, user_id=userid).first()
  return render_template('/workout/workout.html', id=entry_id, workout=workout, workout_stats=workout_stats, username=username, userid=userid)


@workout_blueprint.route('/save_workout/<username>/<int:userid>/<int:entry_id>', methods=['GET', "POST"])
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
      return redirect(url_for('profile.user_home', username=username, userid=userid))


@workout_blueprint.route('/write_updates/<username>/<int:userid>/<int:entry_id>', methods=["GET", "POST"])
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
