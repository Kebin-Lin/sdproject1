import sqlite3

#These functions are meant to be ran from app.py, do not try to use them here.

def registerUser(username, password):

    '''This function creates a user and adds it into the user table.
    '''

    db,c = getDBCursor()
    #Searches if the username already exists
    for i in c.execute("SELECT username FROM users WHERE username = ?",(username,)):
        closeDB(db)
        return "User already exists"
    #Execute if username doesn't exist
    c.execute("INSERT INTO users (username, password) VALUES(?,?)",(username,password,))
    closeDB(db)
    return "Account creation successful"

def auth(username, password):

    '''This function returns a string regarding the status of an attempted login.
    '''

    db,c = getDBCursor()
    #Searches if the user exists
    for i in c.execute("SELECT password FROM users WHERE username = ?",(username,)):
        #Check if passwords match
        if i[0] == password:
            closeDB(db)
            return "Login Successful"
        closeDB(db)
        return "Incorrect Password"
    else:
        closeDB(db)
        return "User does not exist"

def addFriend(username,friendName):

    '''This function adds a friend for a user into the friends table.

    PREREQ: Username exists
    '''

    db,c = getDBCursor()
    #Searches if the friend exists
    for i in c.execute("SELECT username FROM users WHERE username = ?",(friendName,)):
        break
    else:
        closeDB(db)
        return "Friend does not exist"
    #Searches if the user already has the friend added
    for i in c.execute("SELECT friendName FROM friends WHERE friendName = ?",(friendName,)):
        closeDB(db)
        return "Friend already added"
    #Adds friend if not already added
    c.execute("INSERT INTO friends (username, friendName) VALUES(?,?)",(username,friendName,))
    closeDB(db)
    return "Friend successfully added"

def getFriends(username):

    '''Returns a list of friends added by a user
    '''

    output = []
    db,c = getDBCursor()
    #Looks for friends
    for i in c.execute("SELECT friendName FROM friends WHERE username = ?",(username,)):
        #Appends the friends to a list
        output.append(i[0])
    closeDB(db)
    #Returns the list of friends (empty list if user doesn't exist or have any friends)
    return output

def addComment(movieID, comment, username):

    '''This function adds a comment for a movie into the comment table.

    PREREQ: Username exists
    '''

    db,c = getDBCursor()
    #Adds comment
    c.execute("INSERT INTO comments (movieID, comment, username) VALUES(?,?,?)",(movieID, comment, username,))
    closeDB(db)

def getComments(movieID):

    '''Returns a list of comments for a movie
    '''

    output = []
    db,c = getDBCursor()
    #Looks for comments
    for i in c.execute("SELECT comment, username FROM comments WHERE movieID = ?",(movieID,)):
        #Appends the comment information to a list as a tuple (comment, username,)
        output.append((i[0],i[1],))
    closeDB(db)
    #Returns the list of comments (empty list if movie doesn't exist or have any comments)
    return output

def addMovie(username, movieID):

    '''This function adds a liked movie for a user into the moviesAdded table.

    PREREQ: Username exists
    '''

    db,c = getDBCursor()
    #Adds movie
    c.execute("INSERT INTO moviesAdded (username, movieID) VALUES(?,?)",(username, movieID,))
    closeDB(db)

def getMovies(username):

    '''Returns a list of movies that a user has added
    '''

    output = []
    db,c = getDBCursor()
    #Looks for added movies
    for i in c.execute("SELECT movieID FROM moviesAdded WHERE username = ?",(username,)):
        #Appends the movie names to a list
        output.append(i[0])
    closeDB(db)
    #Returns the list of movies (empty list of user doesn't exist or hasn't added any movies)
    return output

def addReview(movieID, review, username, rating):

    '''This function adds a review for a movie into the reviws table.

    PREREQ: Username exists
    '''

    db,c = getDBCursor()
    #Checks if review by user already exists
    for i in c.execute("SELECT username FROM reviews WHERE username = ? AND movieID = ?",(username, movieID,)):
        #If exists, do nothing
        closeDB(db)
        return
    #Adds review
    c.execute("INSERT INTO reviews (username, review, movieID, rating) VALUES(?,?,?,?)",(username, review, movieID, rating,))
    closeDB(db)

def getReviews(movieID):

    '''Returns a list of reviews for a movie
    '''

    output = []
    db,c = getDBCursor()
    #Looks for reviews
    for i in c.execute("SELECT review, username, rating FROM reviews WHERE movieID = ?",(movieID,)):
        #Appends the review information to a list as a tuple (review, username, rating)
        output.append((i[0],i[1],i[2],))
    closeDB(db)
    #Returns the list of reviews (empty list if movie doesn't exist or have any reviews)
    return output

def getRating(movieID):

    '''Returns the average rating of a movie based on the reviews table as a
       string, and returns "N/A" if no ratings have been created.
    '''

    subt = 0
    count = 0
    db,c = getDBCursor()
    #Looks for ratings
    for i in c.execute("SELECT rating FROM reviews WHERE movieID = ?",(movieID,)):
        subt += i[0]
        count += 1
    closeDB(db)
    if count == 0: return "N/A"
    return "%.1f" % (subt / count) #Truncates rating to one decimal

def addMovieInfo(movieID, title, img, plot):

    '''This function adds a OMDB movie ID to a table with the title, image, and
       plot associated to save API calls.
    '''

    db,c = getDBCursor()
    #Adds ID
    c.execute("INSERT INTO movieInfo (movieID, title, img, plot) VALUES(?,?,?,?)",(movieID, title, img, plot,))
    closeDB(db)

def getMovieInfo(movieID):

    '''This function attempts to get the title and image associated with a movie
       ID from the database. It will return None if it does not exist.
    '''

    db,c = getDBCursor()
    output = None
    #Search for ID
    for i in c.execute("SELECT title, img, plot FROM movieInfo WHERE movieID = ?",(movieID,)):
        #Sets output to a tuple (title, img, plot,)
        output = [i[0],i[1],i[2],]
    closeDB(db)
    return output

def getMovieID(title):

    '''This function attempts to get the ID associated with the title of a movie
       and only returns one ID if multiple movies have the same name. If the
       title does not exist in the database, then the function will return None.
    '''

    db,c = getDBCursor()
    output = None
    #Search for title
    for i in c.execute("SELECT movieID FROM movieInfo WHERE title = ? LIMIT 1",(title,)):
        #Sets output to a movieID
        output = i[0]
    closeDB(db)
    return output

def getSortedRatings():

    '''This function returns a list of tuples of ratings and movie IDs sorted in
       order of descending MyNextMovie ratings. Returns an empty list if no
       ratings exist.
    '''

    db,c = getDBCursor()
    output = []
    setMovies = set()
    #Adds all movieIDs of movies that have been rated to a set
    for i in c.execute("SELECT movieID FROM reviews"):
        setMovies.add(i[0])
    closeDB(db)
    #Adds tuples of ratings and movieIDs to the output
    for i in setMovies:
        newTuple = (float(getRating(i)),i)
        output.append(newTuple)
    output.sort(reverse = True) #Sort output
    return output

def getAllUsers():

    '''This function returns a set of all users registered. Returns an empty set
       if no users exist.
    '''

    db,c = getDBCursor()
    output = set()
    #Adds all usernames to the output set
    for i in c.execute("SELECT username FROM users"):
        setMovies.add(i[0])
    closeDB(db)
    return output

def getDBCursor():
    db = sqlite3.connect("data/info.db")
    cursor = db.cursor()
    return db,cursor

def closeDB(db):
    db.commit()
    db.close()
