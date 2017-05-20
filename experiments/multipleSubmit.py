from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)



@app.route('/', methods = ['GET', 'POST'])
def submit():

	if request.method == 'POST':
		print(request.form)
	return render_template("ms.html")




















if __name__ == "__main__":
	app.debug = True
	app.run()