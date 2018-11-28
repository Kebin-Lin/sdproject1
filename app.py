from flask import Flask, render_template, request, session, url_for, redirect,flash
import os,random

from util import apihelp as api
from util import dbtools

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

@app.route("/profile",methods = ["POST", "GET"])
def profile():
	#test movielist
	#if "username" in session:
	#if request.args.get("movie") != None:
	#	query=request.args.get("movie")
	#	dbtools.addMovie(session["username"],api.getOMDBdata(query)["Title"])
	names=["The Dark Knight","Deadpool", "Avengers","The Crow"]
	#when authentication system is working
	#names=dbtools.getMovies(session["username"])
	ml={}
	for name in names:
		ml[name]=api.getOMDBdata(name)
	recm={}
	recommendations=api.getTasteDiveData(names)
	testmovie=recommendations[random.randint(0,9)]["Name"]
	recm=api.getOMDBdata(testmovie)
	return render_template("profile.html",user="me", movielist=ml,recmovie=recm,)

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
