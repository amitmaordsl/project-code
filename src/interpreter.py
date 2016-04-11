import re
import collections
import json

from APIFunctions import rhymesFromWord
from poemHandler import lastWords, filenameToLines

###############
### MAIN functionality
###############

def checkPoem(filename, scheme):
	# take the filename and open it into lines, then last words of lines
	lines = filenameToLines(filename)
	lastWordsList = lastWords(lines)

	# use the last words to create a scheme
	poemScheme = createScheme(lastWordsList)
	return schemeMatcher(scheme, poemScheme)

###############
### POEM functionality
### 
### takes inputs from poem side and interprets
###############

def twoWordsRhyme(word1, word2):
    firstWordStr = rhymesFromWord(word1)
    firstWordJSONThing = json.loads(firstWordStr)
    firstWordWords = map(lambda k: k["word"], firstWordJSONThing)
    
    secondWordStr = rhymesFromWord(word2)
    secondWordJSONThing = json.loads(secondWordStr)
    secondWordWords = map(lambda k: k["word"], secondWordJSONThing)
    return (word2 in firstWordWords) or (word1 in secondWordWords)

def checkRhymes():
	lastWordsList = lastWords(openAndSplit())

	checkWord = lastWordsList[0]
	lastWordsList = lastWordsList[1:]

	for word in lastWordsList:
		if not twoWordsRhyme(word, checkWord):
			print word
			print checkWord
			return False

	return True

###############
### SCHEME functionality
###
### takes inputs from scheme side and interprets
###############
def schemeMatcher(pattern, parsedPattern):
	# matchedPattern = re.match(r'(ab)*', "abababc", flags=0).group()
	matchedPattern = re.match(pattern, parsedPattern, flags=0).group()
	return (matchedPattern == parsedPattern)

def createScheme(words):
    ret = ""
    schemeChar = 'a'
    schemeDict = collections.OrderedDict()

    for word in words:
        # did the word match a rhyme higher in the poem
        trackerHit = False
        # char to be used if a match is found
        trackerChar = ''
        # iterate through the dictionary (in order), checking if the word rhymes with 
        # any word already in the schema. if it does, 
        for key, value in schemeDict.items():
            if twoWordsRhyme(word, value):
                ret += key
                trackerHit = True
                trackerChar = key
                break
        if not trackerHit:
            ret += schemeChar
            schemeDict[schemeChar] = word
            schemeChar = chr(ord(schemeChar) + 1)
        # print ret
    return ret

print(checkPoem("tmp.txt", r'(a*)ba'))
