from flask import Flask, render_template, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from project.models import WorkoutA


@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        workout = WorkoutA(squat_reps='5,3,5,3,5', bench_reps="5,4,3,3,2", row_reps='1,2,3,4,5')
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('save_workout'))
    return render_template('index.html')


@app.route('/save_workout', methods=['GET', "POST"])
def save_workout():
    return "submitted"