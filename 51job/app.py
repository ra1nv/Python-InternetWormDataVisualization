from flask import Flask,render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return index()

@app.route('/job')
def job():
    datalist = []
    con = sqlite3.connect('_51job.db')
    cur = con.cursor()
    sql = 'select * from job'
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template("job.html",jobs=datalist)

@app.route('/area')
def area():
    return render_template("area.html")

@app.route('/salary')
def salary():
    return render_template("salary.html")

@app.route('/word')
def word():
    return render_template("word.html")

if __name__ == '__main__':
    app.run()
