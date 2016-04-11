def tryABunch():
    word = "world"

    # print "rhymebrain"

    # requestStr = "http://rhymebrain.com/talk?function=getRhymes&word=" + word + "&lang=en"
    # print requestStr
    # request = Request(requestStr)
    # response = urlopen(request)
    # readResponse = response.read()
    # print readResponse

    print "azarask"

    requestStr = "http://azarask.in/services/rhyme/?q=" + word

    try:
        response = urlopen(request)
        readResponse = response.read()
        return readResponse
    except URLError, e:
        print 'No kittez. Got an error code:', e
        
    print requestStr
    request = Request(requestStr)
    response = urlopen(request)
    readResponse = response.read()
    print readResponse