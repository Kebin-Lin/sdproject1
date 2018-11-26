from flask import Flask, render_template, request, session, url_for, redirect
import os,random

from util import apihelp as api

app = Flask(__name__)
app.secret_key = os.urandom(32)



@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	#print(api.getOMDbURL('Kung Fury', 1))
	return render_template('homepage.html')

@app.route("/profile",methods = ["POST", "GET"])
def profile():
	#test movielist
	names=["The Dark Knight","Monty Python and the Holy Grail", "Shining","Hot Fuzz"]
	ml={}
	for name in names:
		ml[name]=api.getOMDBdata(name)
	recm={}
	recommendations=api.getTasteDiveData(names)
	testmovie=recommendations[random.randint(0,9)]["Name"]
	recm=api.getOMDBdata(testmovie)
	return render_template("profile.html",user="me", movielist=ml,recmovie=recm,)

if __name__ == "__main__":
	app.debug = True
	app.run()
# API INFO:
	# TasteDive: 324021-MyNextMo-WHLW4A5Z
# our email: mynextmovieapp@gmail.com password: stuysoftdev1
