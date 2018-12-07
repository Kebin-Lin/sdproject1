
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
	'''
		The profile route does multiple tasks:
		1. When a movie is added the id of the movie is sent to this route to be added to the database
		2. If the user has no movies he/she will be redirect to add_movies to add at least one movie
		3. If the user has at least one movie the movielist is compiled from the database and displayed
		4. That movie list is used to get 5 recommendations
		5. These recommendations are also stored into the database
	'''
	#print("This is running")
	#test movielist
	if "username" in session:
		currUserProfile = session["username"]
		if "user" in request.args:
			currUserProfile = request.args.get("user")
			movielist=db.getMovies(currUserProfile)
			if movielist == []:
				flash("This user does not have any movies")
				return redirect(url_for("friends_page"))
		# 1.
		if "add" in request.form:
			query=request.form["add"]
			db.addMovie(session["username"],query)
		if "remove" in request.form:
			query=request.form["remove"]
			db.removeMovie(session["username"],query)
		movielist=db.getMovies(currUserProfile)

		# 2.
		if movielist == []:
			return redirect(url_for("add_movies"))

		#3.
		ids=db.getMovies(currUserProfile)
		print(ids)
		names=[]
		ml={}
		for id in ids:
			if db.getMovieInfo(id) == None:
				data=api.getOMDBdata(id,True)
				db.addMovieInfo(id,data["Title"],data["Poster"],data["Plot"])
			ml[id]=db.getMovieInfo(id)
			names.append(ml[id][0])
		#4.

		recommendedmovie={}
		first_rec_dict={}
		if names != []:
			testmovie=[]
			recommendations=api.getTasteDiveData(names)
			i=0
			try:
				testmovie=(recommendations[i]["Name"])
			#first_rec=recommendations[i]["Name"]
				first_rec_dict=api.getOMDBdata(testmovie,False)
				i+=1
				while i < 5:
					testmovie=(recommendations[i]["Name"])
					mid=db.getMovieID(testmovie)

					# 5.
					if db.getMovieInfo(mid) == None:
						dat=api.getOMDBdata(testmovie,False)
						db.addMovieInfo(dat["imdbID"],dat["Title"],dat["Poster"],dat["Plot"])
						testmovie=dat["Title"]

					currID = db.getMovieID(testmovie)
					recommendedmovie[testmovie]=db.getMovieInfo(currID)
					recommendedmovie[testmovie].append(currID)
					print(recommendedmovie[testmovie])
					i+=1
				print(recommendedmovie)
				#print(f_rec)
			
				return render_template("profile.html",user=currUserProfile, movielist=ml,recmovies=recommendedmovie,f_rec=first_rec_dict)
			except:
				return render_template("err.html")
	else:
		return redirect(url_for("input_field_page"))

@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	'''
		The main route which redirects to the login page if not logged in.
		If the user has no movies it will redirect to addmovies otherwise it will send the user to the profile page
	'''
	# session.clear()
	if "username" in session:
		#debugPrint("logged in as " + session["username"])
		movielist=db.getMovies(session["username"])
		if movielist == []:
			return redirect(url_for("add_movies"))
		else:
			return redirect(url_for("profile_method"))
	#print(api.getOMDbURL('Kung Fury', 1))
	return render_template('homepage.html')

@app.route("/addmovie",methods = ["GET","POST"])
def add_movies():
	'''
		This page returns search results for movies user search using the search bar
	'''
	if "username" in session:
		query=""
		movielist=db.getMovies(session["username"])
		if movielist == [] and "movie" not in request.args :
			flash("Please Add At Least One Movie To Get Recommendations")
			return render_template("addmovie.html")
		results=[]
		print(query)
		if "movie" in request.args:
			query=request.args.get("movie")
		print(query)
		try:
			results=api.getOMDBsearch(query)
		except:
			flash("Please enter a valid search")
		return render_template("addmovie.html",searchresults=results)
	else:
		return redirect(url_for("input_field_page"))
@app.route("/friends",methods = ["GET","POST"])
def friends_page():
	'''
		This route allows the user to add friends who have similar tastes
		The user can also view their lists.
		The user can also see a list of other users
	'''
	if "username" in session:
		userlist=db.getAllUsers()
		if "add" in request.form:
			db.addFriend(session["username"],request.form["add"])
		if "remove" in request.form:
			db.removeFriend(session["username"],request.form["remove"])
		friendlist=db.getFriends(session["username"])
		userlist=[x for x in userlist if (x not in friendlist)] # creates a list of users who aren't friends
		userlist.remove(session["username"])
		return render_template("friendlist.html",friendlist=friendlist,userlist=userlist)
	else:
		return redirect(url_for("input_field_page"))
		

@app.route("/createaccount", methods=["POST"])
def create_account():
	'''
		This route is used for registration
	'''
	if (request.form['password'] == request.form['passwordConfirmation']):
		flash(db.registerUser(request.form['username'], request.form['password']))
		return redirect(url_for("input_field_page"))
	else:
		flash("Password do not match")
	return redirect(url_for("input_field_page"))

@app.route("/auth", methods=["POST"])
def auth_account():
	'''
		Verifies the username and password with the database
	'''
	message = db.auth(request.form["username"], request.form["password"])
	if message == "Login Successful":
		session["username"] = request.form["username"]
	else:
		flash(message)
	return redirect(url_for("input_field_page"))

@app.route("/movie",methods=["POST","GET"])
def movie_info():
	'''
		Users can see info about a movie on this page
		They can also comment and review these movies on this page
		They can add the movie from the page as well
	'''
	if "username" in session:
		if "title" in request.form:
			name=request.form["title"]
		if "add" in request.form:
			query=request.form["add"]
			db.addMovie(session["username"],query)
			name=query
		if "review_remove" in request.form:
			query=request.form["review_remove"]
			db.removeReview(query,session["username"])
			name=query
		if "comment_remove" in request.form:
			query=request.form["comment_remove"].split("&")[0]
			comment=request.form["comment_remove"].split("&")[1]
			db.removeComment(query,comment,session["username"])
			name=query
		if db.getMovieInfo(name) == None:
			data=api.getOMDBdata(name,True)
			print(data)
			db.addMovieInfo(name,data["Title"],data["Poster"],data["Plot"])
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
	'''
		Pops the user out of session
	'''
	if "username" in session:
		session.pop("username")
	return redirect(url_for("input_field_page"))

@app.route("/discover")
def discoverPage():
	'''
		Displays movies sorted by the ratings on our site
	'''
	ratings = db.getSortedRatings()
	toDisplay = []
	#Grabs titles of sorted movieIDs
	for i in ratings:
		movieInfo = db.getMovieInfo(i[1])
		print(movieInfo)
		newTuple = (i[0],i[1],movieInfo[0],movieInfo[1])
		toDisplay.append(newTuple)
	return render_template("discover.html",movieList = toDisplay)

@app.route("/about")
def aboutPage():
	'''
		Gives information about our website
	'''
	return render_template("about.html")

if __name__ == "__main__":
	app.debug = True
	app.run()
# API INFO:
	# TasteDive: 324021-MyNextMo-WHLW4A5Z
# our email: mynextmovieapp@gmail.com password: stuysoftdev1
