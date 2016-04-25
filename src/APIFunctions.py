from urllib2 import Request, urlopen, URLError

### Returns a JSON of the rhymes to a given word
### input: a word (string)
### output: a JSON string of the words rhyming with that word
def rhymesFromWord(word, count):
    requestStr = "https://api.datamuse.com/words?rel_rhy=" + word + "&max=" + str(count)
    request = Request(requestStr)

    try:
        response = urlopen(request)
        readResponse = response.read()
        return readResponse
    except URLError, e:
        print 'Bad API request. Got an error code:', e