TasteDiveApiKey = '324021-MyNextMo-WHLW4A5Z'
OMDbApiKey = '555fca05'
def getTasteDiveURL (movies):
	url = "https://tastedive.com/api/similar?q="
	for movieTitle in movies:
		url += 'movie:' + movieTitle + ','
	url = url[:-1]
	url += '&k=' + TasteDiveApiKey
	return url

def getOMDbURL (searchQuery, pageNum):
	searchTerms = searchQuery.split(' ')
	searchUrl = '+'.join(searchTerms)
	url = 'https://omdbapi.com/?s=' + searchUrl + '&page=' + str(pageNum) + '&apikey=' + OMDbApiKey
	return url