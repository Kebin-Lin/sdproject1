from flask import Flask, render_template, request, session, url_for, redirect
import os

from util import apihelp as api

app = Flask(__name__)
app.secret_key = os.urandom(32)



@app.route("/", methods = ["POST", "GET"])
def input_field_page():
	#print(api.getOMDbURL('Kung Fury', 1))
	return render_template('homepage.html')

if __name__ == "__main__":
	app.debug = True
	app.run()
# API INFO:
	# TasteDive: 324021-MyNextMo-WHLW4A5Z
# our email: mynextmovieapp@gmail.com password: stuysoftdev1
