from project import db

class WorkoutA(db.Model):
    __tablename__ = 'a_exercises'

    entry_id = db.Column(db.Integer, primary_key=True)
    squat_reps = db.Column(db.String, nullable=True)
    bench_reps = db.Column(db.String, nullable=True)
    row_reps = db.Column(db.String, nullable=True)

    def __init__(self, squat_reps, bench_reps, row_reps):
        self.squat_reps = squat_reps
        self.bench_reps = bench_reps
        self.row_reps = row_reps

    def __repr__(self):
        return "Squat: {}, Bench: {}, Row: {}".format(self.squat_reps, self.bench_reps, self.row_reps)

