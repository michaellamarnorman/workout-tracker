from project import db
from project.models import WorkoutA

db.create_all()

workout_1 = WorkoutA(squat_reps="5,4,5,5,5", bench_reps="5,5,5,5,3", row_reps="5,5,3,4,4")
db.session.add(workout_1)
db.session.commit()