import re
import collections
import json

from APIFunctions import rhymesFromWord
from poemHandler import lastWords, filenameToLines

###############
### MAIN functionality
###############

schemeDict = collections.OrderedDict()

def checkPoem(filename, scheme):
    # take the filename and open it into lines, then last words of lines
    lines = filenameToLines(filename)
    lastWordsList = lastWords(lines)

    # use the last words to create a scheme
    poemScheme = createScheme(lastWordsList)
    return schemeParser(scheme, poemScheme, lastWordsList)

###############
### POEM functionality
### 
### takes inputs from poem side and interprets
###############

def rhymeListFromWord(word):
    wordStr = rhymesFromWord(word)
    wordJSONThing = json.loads(wordStr)
    return map(lambda k: k["word"], wordJSONThing)

def twoWordsRhyme(word1, word2):
    firstWordWords = rhymeListFromWord(word1)
    
    secondWordWords = rhymeListFromWord(word2)
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
def schemeParser(pattern, parsedPattern, lastWordsList):
    parsedPatternIndex = 0
    while (not (not pattern)):
        # run into paren
        if (pattern[0] == '('):
            endBrace = pattern.find(')')
            tempPattern = pattern[1:endBrace]
            
            # the parsed pattern matches the parens pattern
            while (tempPattern == parsedPattern[:len(tempPattern)]):
                parsedPattern = parsedPattern[len(tempPattern):]
                parsedPatternIndex = parsedPatternIndex + len(tempPattern)

            pattern = pattern[endBrace+1:]
        # here, you match a single character in the pattern to a single char in the parsed pattern 
        # then you recurse
        else:
            if (pattern[0] == parsedPattern[0]):
                pattern = pattern[1:]
                parsedPattern = parsedPattern[1:]
                parsedPatternIndex = parsedPatternIndex + 1
            else:
                print "Poem did not match specified scheme!"
                print "incorrect line is line " + str(parsedPatternIndex) + ", with last word: " + lastWordsList[parsedPatternIndex]
                print "the correct word should rhyme with " + schemeDict[pattern[0]]
                print "rhyme suggestions: " + ', '.join(rhymeListFromWord(schemeDict[pattern[0]]))
                print "Current letter assignments:", json.dumps(schemeDict, indent=4)
                return
    return (not pattern) and (not parsedPattern)


def createScheme(words):
    ret = ""
    schemeChar = 'a'

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

print(checkPoem("tmp.txt", r'(a)bba'))
