from project import db
import datetime


class WorkoutA(db.Model):
    __tablename__ = 'a_exercises'

    entry_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default = datetime.datetime.now)
    squat_reps = db.Column(db.String, nullable=True)
    bench_reps = db.Column(db.String, nullable=True)
    row_reps = db.Column(db.String, nullable=True)
    press_reps = db.Column(db.String, nullable=True)
    deadlift_reps = db.Column(db.String, nullable=True)
    squat_weight = db.Column(db.Integer, nullable=True)
    bench_weight = db.Column(db.Integer, nullable=True)
    row_weight = db.Column(db.Integer, nullable=True)
    press_weight = db.Column(db.Integer, nullable=True)
    deadlift_weight = db.Column(db.Integer, nullable=True)
    squat_sets = db.Column(db.Integer, nullable=True)
    bench_sets = db.Column(db.Integer, nullable=True)
    row_sets = db.Column(db.Integer, nullable=True)
    press_sets = db.Column(db.Integer, nullable=True)
    deadlift_sets = db.Column(db.Integer, nullable=True)
    workout_a_b = db.Column(db.String, nullable=False)
    workout_complete = db.Column(db.Integer, nullable=False)

    def __init__(self, start_time = datetime.datetime.now, squat_reps="",
        bench_reps="", row_reps="", press_reps="", deadlift_reps="",
        squat_weight=None, bench_weight=None, row_weight=None, 
        press_weight=None, deadlift_weight=None, squat_sets=None,
        bench_sets=None,  row_sets=None,  press_sets=None,  deadlift_sets=None,
        workout_a_b='A', workout_complete=0):
        self.squat_reps = squat_reps
        self.bench_reps = bench_reps
        self.row_reps = row_reps
        self.press_reps = press_reps
        self.deadlift_reps = deadlift_reps
        self.squat_weight = squat_weight
        self.bench_weight = bench_weight
        self.row_weight = row_weight
        self.press_weight = press_weight
        self.deadlift_weight = deadlift_weight
        self.squat_sets = squat_sets
        self.bench_sets = bench_sets
        self.row_sets = row_sets
        self.press_sets = press_sets
        self.deadlift_sets = deadlift_sets
        self.workout_a_b = workout_a_b
        self.workout_complete = workout_complete

    def __repr__(self):
        return "Squat: {}, Bench: {}, Row: {}".format(self.squat_reps, self.bench_reps, self.row_reps)

