from flask import Flask, render_template, request, redirect, url_for, session
import csv
import json

app = Flask(__name__)


@app.route('/')
def index():
    gsaCSV = []
    with open("usjoin.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            gsaCSV.append(row)

    with open('mymap.svg', 'r') as myfile:
        data = myfile.read()
    #print(data.replace('"', "'"))
    data = data.replace('"', "'")
    return render_template("html-in-div.html",
                           gsaCSV=json.dumps(gsaCSV), mymap=json.dumps(data))


if __name__ == "__main__":
    app.debug = True
    app.run()
