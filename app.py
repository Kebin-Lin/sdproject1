from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
import random
from util import dbtools as db
from util import apihelp as api

app = Flask(__name__)
app.secret_key = os.urandom(32)

hardcodedUser = {"username": "test", "password": "test"}


def debugPrint(toPrint):
	print("--------------------------")
	print(toPrint)
	print("--------------------------")

@app.route("/profile",methods = ["POST", "GET"])
def profile_method():
	print("This is running")
	#test movielist
	if "username" in session:
		name = []
		if request.args.get("movie") != None:
			query=request.args.get("movie")
			db.addMovie(session["username"],api.getOMDBdata(query)["Title"])
		names=db.getMovies(session["username"])
		ml={}
		for name in names:
			ml[name]=api.getOMDBdata(name)
		recm={}
		# recommendations=api.getTasteDiveData(names)
		# # testmovie=recommendations[random.randint(0,9)]["Name"]
		# recm=api.getOMDBdata(testmovie)
		return render_template("profile.html",user="me", movielist=ml,recmovie=recm,)
	else:
		return redirect(url_for("input_field_page"))

@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	# session.clear()
	if "username" in session:
		debugPrint("logged in as " + session["username"])
		return redirect(url_for("profile_method"))
	#print(api.getOMDbURL('Kung Fury', 1))
	return render_template('homepage.html')

@app.route("/addmovie",methods = ["GET","POST"])
def add_movies():
	query=""
	results=[]
	if request.args.get("movie") != None:
		query=request.args.get("movie")
		results=api.getOMDBsearch(query)
	return render_template("addmovie.html",searchresults=results)

@app.route("/auth", methods=["POST"])
def auth_account():
	if db.auth(request.form["username"], request.form["password"]):
		debugPrint("Successful Login")
		session["username"] = request.form["username"]
	else:
		debugPrint("Failed Login")
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
		if fakeCheckIfUserInDB(request.form['username']):
			flash("Username already taken")
			return render_template('homepage.html')
		else:
			flash("Account created successfully")
			db.registerUser(request.form['username'], request.form['password'])
			return redirect(url_for("input_field_page"))
	else:
		flash("Password do not match")
	return redirect(url_for("input_field_page"))


def fakeCheckIfUserInDB(username):
	return username == "test"

def _temp_login(username, password):
	return username == hardcodedUser["username"] and password == hardcodedUser["password"]

if __name__ == "__main__":
	app.debug = True
	app.run()
# API INFO:
	# TasteDive: 324021-MyNextMo-WHLW4A5Z
# our email: mynextmovieapp@gmail.com password: stuysoftdev1
