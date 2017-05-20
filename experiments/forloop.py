from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)


@app.route('/<int:i>')
def forloop(i):
	l=[]
	for x in range(i):
		l.append(str(x))
	return render_template("forloop.html", l=l)







if __name__ == "__main__":
	app.debug = True
	app.run()