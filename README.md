# Hackstreet Boys
Kevin Lin (Project Manager), Mohammed Jamil, Tianrun Liu, Sajed Nahian
### Summary
Our project allows the user to create a profile and add a list of movies they
like to it. The program will generate new movie recommendations based on what
you like. You will also be able to leave reviews for movies and generate
recommendations from other user profiles.

## Running the Application
Notes:
* This application uses Python 3
* Requires a virtual environment or permission to install packages

Creating a virtual environment:
```
python3 -m venv <Name>
```

Activating a virtual environment:
```
. <path to venv>/bin/activate
```

On Windows:
```
. <path to venv>/Scripts/activate
```

Installing requirements:
```
pip install -r requirements.txt
```
Make sure this is done in the same directory as requirements.txt.

Launching the application:
```
python app.py
```

List of Dependencies:
- Flask: Serves the page for the user.
- Wheel: Flask is dependent on wheel.
- URLLib3: Allows for the interaction with APIs.

### API Info
OMDb: Used to get movie info such as the movie poster and description. Also
provides a movie ID to distinguish movies with similar names. An API key can be
obtained [here](http://www.omdbapi.com/apikey.aspx).

TasteDive: Takes movie(s) as the input and recommends new movies. An API key can
be obtained by creating an account and requesting a key [here](https://tastedive.com/account/api_access).

If you want to use your keys to run the application, go to util/apihelp.py and
replace the string values for TasteDiveApiKey and OMDbApiKey with your own keys.
