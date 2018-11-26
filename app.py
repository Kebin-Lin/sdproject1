from flask import Flask, render_template, request, session, url_for, redirect, flash
import os

from util import apihelp as api

app = Flask(__name__)
app.secret_key = os.urandom(32)

hardcodedUser = {"username": "test", "password": "test"}


def debugPrint(toPrint):
	print("--------------------------")
	print(toPrint)
	print("--------------------------")

@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	#session.clear()
	if "username" in session:
		debugPrint("logged in as " + session["username"])
	#print(api.getOMDbURL('Kung Fury', 1))
	return render_template('homepage.html')

@app.route("/auth", methods=["POST"])
def auth_account():
	if _temp_login(request.form["username"], request.form["password"]):
		session["username"] = request.form["username"]
	else:
		flash("Invalid Login Credentials")
	return redirect(url_for("input_field_page"))

@app.route("/signup", methods=["POST", "GET"])
def sign_up_page ():
	if "username" in session:
		return render_template("homepage")
	return render_template("signup.html")

@app.route("/createaccount", methods=["POST"])
def create_account():
	if (request.form['password'] == request.form['passwordConfirmation']):
		if not(True):
			flash("Username already taken")
			return redirect(url_for("sign_up_page"))
		else:
			flash("Account created successfully")
			return redirect(url_for("input_field_page"))
	else:
		flash("Password do not match")
return redirect(url_for("sign_up_page"))

def _temp_login(username, password):
	return username == hardcodedUser["username"] and password == hardcodedUser["password"]
	
if __name__ == "__main__":
	app.debug = True
	app.run()
# API INFO:
	# TasteDive: 324021-MyNextMo-WHLW4A5Z
# our email: mynextmovieapp@gmail.com password: stuysoftdev1
