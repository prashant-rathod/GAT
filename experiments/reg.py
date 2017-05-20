from flask import Flask, render_template, request, redirect, url_for, session
import os
import json


application = Flask(__name__)
fileDict = {}
tempdir = 'static/temp/'

@application.route('/')
def regionalization():
	with open('mymap.svg', 'r') as myfile:
		data = myfile.read()
	#print(data.replace('"', "'"))
	data = data.replace('"', "'")
	return render_template("regionalization.html", mymap = data)



application.secret_key = 'na3928ewafds'


if __name__ == "__main__":
	application.debug = True
	application.run()