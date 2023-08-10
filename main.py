import csv

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TimeField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = "ronaldihno"
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    opening_time = TimeField('Opening Time', validators=[DataRequired()])
    closing_time = TimeField('Closing Time', validators=[DataRequired()])
    coffee = SelectField("Coffee", [DataRequired()], choices=["★", "★★", "★★★", "★★★★", "★★★★★"])
    wifi = SelectField("WiFi", choices=["Yes", "No"])
    Power = SelectField("Power", choices=["Yes", "No"])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafe-list')
def cafe_list():
    with open("cafe_data.csv", newline='') as file_csv:
        data = csv.reader(file_csv, delimiter=',')
        list_of_rows = []
        for row in data:
            list_of_rows.append(row)
    return render_template('list.html', data=list_of_rows)


@app.route("/add")
def add_to_list():
    form = CafeForm()
    if form.validate_on_submit():
        f = open("cafe_data.csv", "a")
        form_list = [form.cafe_name.data,
                     form.location.data,
                     str(form.opening_time.data),
                     str(form.closing_time.data),
                     form.coffee.data,
                     form.wifi.data,
                     form.Power.data]
        form_1 = ",".join(form_list)
        f.writelines(f"\n{form_1}")
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
