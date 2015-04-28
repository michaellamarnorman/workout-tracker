from project import db
from project.models import WorkoutA

db.create_all()

workout_1 = WorkoutA(squat_reps="5,4,5,5,5", bench_reps="5,5,5,5,3",
  row_reps="5,5,3,4,4", squat_weight=195, bench_weight=135, row_weight=115, 
  press_weight=95, deadlift_weight=225, squat_sets=25,bench_sets=25,
  row_sets=25,  press_sets=25,  deadlift_sets=5, workout_a_b='A', workout_complete=1)
db.session.add(workout_1)
db.session.commit()