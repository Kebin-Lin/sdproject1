import urllib.request as urlrequest
import urllib.parse as parse
import json

TasteDiveApiKey = '324021-MyNextMo-WHLW4A5Z'
OMDbApiKey = '555fca05'
def getTasteDiveURL (movies):
	url = "https://tastedive.com/api/similar?q="
	for movieTitle in movies:
		searchTerms = movieTitle.split(' ')
		searchUrl = '+'.join(searchTerms)
		url += 'movie:' + searchUrl + ','
	url = url[:-1]
	url += '&k=' + TasteDiveApiKey
	return url
def getTasteDiveData(movies):
	recurl=getTasteDiveURL(movies)
	req=urlrequest.Request(recurl,headers={'User-Agent': 'Mozilla/5.0'})
	urlobj=urlrequest.urlopen(req)
	data=json.load(urlobj)
	return data["Similar"]["Results"]

def getOMDbURL (searchQuery, pageNum):
	searchTerms = searchQuery.split(' ')
	searchUrl = '+'.join(searchTerms)
	url = 'https://omdbapi.com/?s=' + searchUrl + '&page=' + str(pageNum) + '&apikey=' + OMDbApiKey
	return url

def getOMDBpage(searchQuery):
	search=getOMDbURL(searchQuery,1)
	req=urlrequest.Request(search,headers={'User-Agent': 'Mozilla/5.0'})
	urlobj=urlrequest.urlopen(req)
	searchdata=json.load(urlobj)
	name=searchdata["Search"][0]["Title"]
	searchTerms = name.split(' ')
	searchUrl = '+'.join(searchTerms)
	url = "https://omdbapi.com/?t=" + searchUrl + "&apikey=" + OMDbApiKey
	return url

def getOMDBdata(searchQuery):
	moviedata={"Title":"","Plot":"","Poster":""}
	movieurl=getOMDBpage(searchQuery)
	req=urlrequest.Request(movieurl,headers={'User-Agent': 'Mozilla/5.0'})
	urlobj=urlrequest.urlopen(req)
	data=json.load(urlobj)
	for keys in moviedata:
		moviedata[keys]=data[keys]
	return moviedata
		


	