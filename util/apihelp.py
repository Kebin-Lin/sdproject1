import urllib.request as urlrequest
import urllib.parse as parse
import json

#Sets API keys
with open("data/keys.json") as keyFile:
	APIKeys = json.loads(keyFile.read())

TasteDiveApiKey = APIKeys['TasteDiveApiKey']
OMDbApiKey = APIKeys['OMDbApiKey']

def getTasteDiveURL (movies):
	'''
		This function uses the APIKey shown above to return a url to data on the similar movies found by TasteDive
	'''
	url = "https://tastedive.com/api/similar?q="
	for movieTitle in movies:
		searchUrl = urlrequest.quote(movieTitle)
		url += 'movie:' + searchUrl + ','
	url = url[:-1]
	url += '&k=' + TasteDiveApiKey +"&type=movies"
	return url
def getTasteDiveData(movies):
	'''
		This function extracts the data from the JSON file from the url acquired by getTasteDiveURL
	'''
	recurl=getTasteDiveURL(movies)
	req=urlrequest.Request(recurl,headers={'User-Agent': 'Mozilla/5.0'})
	urlobj=urlrequest.urlopen(req)
	data=json.load(urlobj)
	return data["Similar"]["Results"]

def getOMDbURL (searchQuery, pageNum):
	'''
		Returns the url to certain page of search results on OMDB that match the searchQuery
	'''
	searchUrl = urlrequest.quote(searchQuery)
	url = 'https://omdbapi.com/?s=' + searchUrl + '&page=' + str(pageNum) + '&apikey=' + OMDbApiKey +"&type=movie"
	return url

def getOMDBsearch(searchQuery):
	url=getOMDbURL(searchQuery,1)
	req=urlrequest.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
	urlobj=urlrequest.urlopen(req)
	searchresults=json.load(urlobj)
	return searchresults["Search"]

def getOMDBpage(searchQuery,isID):
	'''
		Returns the OMDB url for the first searh result
	'''
	if isID:
		url = "https://omdbapi.com/?i=" + searchQuery + "&apikey=" + OMDbApiKey +"&type=movie"
	else:
		searchUrl=urlrequest.quote(searchQuery)
		url = "https://omdbapi.com/?t=" + searchUrl + "&apikey=" + OMDbApiKey
	return url

def getOMDBdata(searchQuery,isID):
	'''
		Returns the title,plot and poster of a movie from the url returned by getOMDBpage
	'''
	moviedata={"Title":"","Plot":"","Poster":"","imdbRating":"","Metascore":""}
	movieurl=getOMDBpage(searchQuery,isID)
	req=urlrequest.Request(movieurl,headers={'User-Agent': 'Mozilla/5.0'})
	urlobj=urlrequest.urlopen(req)
	data=json.load(urlobj)
	for keys in moviedata:
		moviedata[keys]=data[keys]
	return moviedata
def getOMDBdata_all(searchQuery,isID):
	movieurl=getOMDBpage(searchQuery,isID)
	req=urlrequest.Request(movieurl,headers={'User-Agent': 'Mozilla/5.0'})
	urlobj=urlrequest.urlopen(req)
	data=json.load(urlobj)
	return data
