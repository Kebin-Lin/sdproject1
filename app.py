from flask import Flask, render_template, request, session, url_for, redirect
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

TasteDiveApiKey = '324021-MyNextMo-WHLW4A5Z'
OMDbApiKey = '555fca05'

@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	# print(getOMDbURL('Kung Fury', 1))
	return render_template('homepage.html')

def getTasteDiveURL (movies):
	url = "https://tastedive.com/api/similar?q="
	for movieTitle in movies:
		url += 'movie:' + movieTitle + ','
	url = url[:-1]
	url += '&k=' + TasteDiveApiKey

def getOMDbURL (searchQuery, pageNum):
	searchTerms = searchQuery.split(' ')
	searchUrl = '+'.join(searchTerms)
	url = 'https://omdbapi.com/?s=' + searchUrl + '&page=' + str(pageNum) + '&apikey=' + OMDbApiKey
	return url

if __name__ == "__main__":
	app.debug = True
	app.run()
# API INFO:
	# TasteDive: 324021-MyNextMo-WHLW4A5Z
# our email: mynextmovieapp@gmail.com password: stuysoftdev1
