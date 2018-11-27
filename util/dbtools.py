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
    c.execute("INSERT INTO users (username, password) VALUES(?,?)")
    closeDB(db)
    return "Account creation successful"

def auth(username, password):

    '''This function returns a string regarding the status of an attempted login.
    '''

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

def addComment(movieName, comment, username):

    '''This function adds a comment for a movie into the comment table.

    PREREQ: Username exists
    '''

    db,c = getDBCursor()
    #Adds comment
    c.execute("INSERT INTO comments (movieName, comment, username) VALUES(?,?,?)",(movieName, comment, username,))
    closeDB(db)

def getComments(movieName):

    '''Returns a list of comments for a movie
    '''

    output = []
    db,c = getDBCursor()
    #Looks for comments
    for i in c.execute("SELECT comment, username FROM comments WHERE movieName = ?",(movieName,)):
        #Appends the comment information to a list as a tuple (comment, username,)
        output.append((i[0],i[1],))
    closeDB(db)
    #Returns the list of comments (empty list if movie doesn't exist or have any comments)
    return output

def addMovie(username, movieName):

    '''This function adds a liked movie for a user into the moviesAdded table.

    PREREQ: Username exists
    '''

    db,c = getDBCursor()
    #Adds movie
    c.execute("INSERT INTO moviesAdded (username, movieName) VALUES(?,?)",(username, movieName,))
    closeDB(db)

def getMovies(username):

    '''Returns a list of movies that a user has added
    '''

    output = []
    db,c = getDBCursor()
    #Looks for added movies
    for i in c.execute("SELECT movieName FROM moviesAdded WHERE username = ?",(username,)):
        #Appends the movie names to a list
        output.append(i[0])
    closeDB(db)
    #Returns the list of movies (empty list of user doesn't exist or hasn't added any movies)
    return output

def addReview(movieName, review, username, rating):

    '''This function adds a review for a movie into the reviws table.

    PREREQ: Username exists
    '''

    db,c = getDBCursor()
    #Adds review
    c.execute("INSERT INTO reviews (username, review, movieName, rating) VALUES(?,?,?,?)",(username, review, movieName, rating,))
    closeDB(db)

def getReviews(movieName):

    '''Returns a list of reviews for a movie
    '''

    output = []
    db,c = getDBCursor()
    #Looks for reviews
    for i in c.execute("SELECT review, username FROM comments WHERE movieName = ?",(movieName,)):
        #Appends the review information to a list as a tuple (review, username,)
        output.append((i[0],i[1],))
    closeDB(db)
    #Returns the list of reviews (empty list if movie doesn't exist or have any reviews)
    return output

def getDBCursor():
    db = sqlite3.connect("data/info.db")
    cursor = db.cursor()
    return db,cursor

def closeDB(inDB):
    db.commit()
    db.close()
