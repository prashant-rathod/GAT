from flask import Flask, url_for, redirect, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def hello_world():
	return ("Hello, World!")

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name = None):
	return render_template('hello.html', name=name)

#user input via URL
@app.route('/user/<username>')
def welcome(username):
	return "Welcome, " + username

@app.route('/post/<int:post_int>')
def dispNum(post_int):
	return "Post number * 2 = " + str(post_int*2)

#redirection
@app.route('/redirect/')
def red():
	return redirect(url_for('hello_world'))

# URL building

