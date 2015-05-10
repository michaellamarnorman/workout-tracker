from flask import flash, Blueprint, url_for, redirect, request, render_template
from project import app, db
from flask.ext.login import login_required
from project.models import User, WorkoutA
from project import find_previous_and_current_workout


profile_blueprint = Blueprint(
    'profile',
    __name__,
    url_prefix="/profile",
    template_folder="templates",
    static_folder="static"
    )



@profile_blueprint.route('/<username>/<int:userid>/home', methods=["GET", "POST"])
@login_required
def user_home(username, userid):
  previous_stats, next_workout = find_previous_and_current_workout(user_id=userid)
  ongoing_workout = db.session.query(WorkoutA).filter_by(workout_complete=0, user_id=userid).order_by(WorkoutA.entry_id.desc()).first()

  if request.method == 'POST':
    if ongoing_workout:
      return redirect(url_for('workout.workout', entry_id=ongoing_workout.entry_id, username=username, userid=userid, workout=ongoing_workout.workout_a_b))
 
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
    return redirect(url_for('workout.workout', entry_id=id.entry_id, workout=id.workout_a_b, username=username, userid=userid))

  if ongoing_workout:
    return render_template('/profile/user_home.html', prev_stats=previous_stats, ongoing_workout=ongoing_workout)

  return render_template('/profile/user_home.html', prev_stats = previous_stats, next_stats=next_workout)
