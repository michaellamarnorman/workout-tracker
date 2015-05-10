from project import db
import datetime




class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='user')
    workouts = db.relationship('WorkoutA', backref="athlete")

    def __init__(self, name=None, email=None, password=None, role=None):
        self.name= name 
        self.email = email
        self.password = password
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


    def __repr__(self):
        return 'User: %s'.format(self.name)



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
    workout_number = db.Column(db.Integer, autoincrement=True , nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, start_time = datetime.datetime.now, squat_reps="",
        bench_reps="", row_reps="", press_reps="", deadlift_reps="",
        squat_weight=45, bench_weight=45, row_weight=45, 
        press_weight=45, deadlift_weight=45, squat_sets=25,
        bench_sets=25,  row_sets=25,  press_sets=25,  deadlift_sets=5,
        workout_a_b='B', workout_complete=0, workout_number=0 , user_id=None):
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
        self.workout_number = workout_number
        self.user_id = user_id

    def __repr__(self):
        return "Squat: {}, Bench: {}, Row: {}".format(self.squat_reps, self.bench_reps, self.row_reps)

