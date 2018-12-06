
import os
import random
import urllib.request as urlrequest

from flask import Flask, render_template, request, session, url_for, redirect, flash
from util import dbtools as db
from util import apihelp as api

app = Flask(__name__)
app.secret_key = os.urandom(32)

hardcodedUser = {"username": "test", "password": "test"}


#def debugPrint(toPrint):
	#print("--------------------------")
	#print(toPrint)
	#print("--------------------------")

@app.route("/profile",methods = ["POST", "GET"])
def profile_method():
	#print("This is running")
	#test movielist
	if "username" in session:

		ids=db.getMovies(session["username"])
		names=[]
		ml={}
		for id in ids:
			if db.getMovieInfo(id) == None:
				data=api.getOMDBdata(id,True)
				db.addMovieInfo(id,data["Title"],data["Poster"],data["Plot"])
			ml[id]=db.getMovieInfo(id)
			names.append(ml[id][0])
		recommendedmovie={}
		first_rec_dict={}
		if names != []:
			testmovie=[]
			recommendations=api.getTasteDiveData(names)
			i=0
			testmovie=(recommendations[i]["Name"])
			#first_rec=recommendations[i]["Name"]
			first_rec_dict=api.getOMDBdata(testmovie,False)
			i+=1
			while i < 5:
				testmovie=(recommendations[i]["Name"])
				recommendedmovie[testmovie]=api.getOMDBdata(testmovie,False)
				recommendedmovie[testmovie]["index"]=i
				i+=1
			#print(f_rec)
		return render_template("profile.html",user=session["username"], movielist=ml,recmovies=recommendedmovie,f_rec=first_rec_dict)
	else:
		return redirect(url_for("input_field_page"))

@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	# session.clear()
	if "username" in session:
		#debugPrint("logged in as " + session["username"])
		movielist=db.getMovies(session["username"])
		print(movielist)
		if movielist == []:
			return redirect(url_for("add_movies"))
		else:
			return redirect(url_for("profile_method"))
	#print(api.getOMDbURL('Kung Fury', 1))
	return render_template('homepage.html')

@app.route("/addmovie",methods = ["GET","POST"])
def add_movies():
	if "username" in session:
		if "add" in request.form:
			query=request.form["add"]
			db.addMovie(session["username"],query)
		movielist=db.getMovies(session["username"])
		print(movielist)
		if movielist == []:
			flash("Please Add At Least One Movie To Get Recommendations")
		query=""
		results=[]
		if request.args.get("movie") != None:
			query=request.args.get("movie")
			try:
				results=api.getOMDBsearch(query)
			except:
				flash("Please enter a valid search")
	return render_template("addmovie.html",searchresults=results)

@app.route("/createaccount", methods=["POST"])
def create_account():
	if (request.form['password'] == request.form['passwordConfirmation']):
		flash(db.registerUser(request.form['username'], request.form['password']))
		return redirect(url_for("input_field_page"))
	else:
		flash("Password do not match")
	return redirect(url_for("input_field_page"))

@app.route("/signup", methods=["POST", "GET"])
def sign_up_page ():
	if "username" in session:
		return render_template("homepage")
	return render_template("signup.html")

@app.route("/auth", methods=["POST"])
def auth_account():
	message = db.auth(request.form["username"], request.form["password"])
	if message == "Login Successful":
		session["username"] = request.form["username"]
	else:
		flash(message)
	return redirect(url_for("input_field_page"))

@app.route("/movie",methods=["POST","GET"])
def movie_info():
	if "username" in session:
		if "add" in request.form:
			query=request.form["add"]
			db.addMovie(session["username"],query)
			name=query
		else:
			name=request.form["title"]
		#print(name)
		print(name)
		data=api.getOMDBdata_all(name,True)
		add=True
		if data["imdbID"] in db.getMovies(session["username"]):
			add=False
		if "comment" in request.form:
			db.addComment(data["imdbID"],request.form["comment"],session["username"])
		comments=db.getComments(data["imdbID"])
		if "review" in request.form:
			db.addReview(data["imdbID"],request.form["review"],session["username"],request.form["rating"])
		reviews=db.getReviews(data["imdbID"])
		rating=db.getRating(data["imdbID"])
		return render_template("info.html",title=name,info=data,comments=comments,user=session["username"],indb=add,reviews=reviews,ourrating=rating)
	else:
		return redirect(url_for("input_field_page"))

@app.route("/logout",methods=["POST","GET"])
def user_logout():
	if "username" in session:
		session.pop("username")
	return redirect(url_for("input_field_page"))


if __name__ == "__main__":
	app.debug = True
	app.run()
# API INFO:
	# TasteDive: 324021-MyNextMo-WHLW4A5Z
# our email: mynextmovieapp@gmail.com password: stuysoftdev1
