# import csv
from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TimeField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
bootstrap = Bootstrap5(app)
db.init_app(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    opening_time = TimeField('Opening Time', validators=[DataRequired()])
    closing_time = TimeField('Closing Time', validators=[DataRequired()])
    coffee = SelectField("Coffee", [DataRequired()], choices=["★", "★★", "★★★", "★★★★", "★★★★★"])
    wifi = SelectField("WiFi", choices=["Yes", "No"])
    Power = SelectField("Power", choices=["Yes", "No"])
    submit = SubmitField('Submit')


class CafeDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, unique=True, nullable=False)
    opening_time = db.Column(db.String, nullable=False)
    closing_time = db.Column(db.String, nullable=False)
    coffee = db.Column(db.String, nullable=False)
    wifi = db.Column(db.String)
    power = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafe-list')
def cafe_list():
    # with open("cafe_data.csv", newline='') as file_csv:
    #     data = csv.reader(file_csv, delimiter=',')
    #     list_of_rows = []
    #     for row in data:
    #         list_of_rows.append(row)
    # data=list_of_rows
    all_cafes = CafeDB.query.all()
    return render_template('list.html', cafes=all_cafes)


@app.route("/add", methods=["POST", "GET"])
def add_to_list():
    form = CafeForm()
    if form.validate_on_submit():
        with app.app_context():
            new_cafe = CafeDB(cafe_name=form.cafe_name.data,
                              location=form.location.data,
                              opening_time=str(form.opening_time.data),
                              closing_time=str(form.closing_time.data),
                              coffee=form.coffee.data,
                              wifi=form.wifi.data,
                              power=form.Power.data)
            db.session.add(new_cafe)
            db.session.commit()
        redirect("/list")
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
