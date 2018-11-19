from flask import Flask, render_template, request, session, url_for, redirect
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	return render_template('homepage.html')

if __name__ == "__main__":
	app.debug = True
	app.run()
