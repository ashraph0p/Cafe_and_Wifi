import csv

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


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


if __name__ == '__main__':
    app.run(debug=True)
