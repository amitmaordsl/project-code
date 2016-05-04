import collections
import json

from APIFunctions import rhymesFromWord
from errorMessages import didNotMatchScheme, notSameLetters, someLinesNotParsed

# Check if the form contains appropriate parentheticals and only alphanumerics otherwise
def checkValidForm(form):
    while not (not form):
        closeParen = form.find(")")
        openParen = form.find("(")
        # no parens
        if (closeParen == -1 and openParen == -1):
            print "Valid rhyme scheme!"
            return True
        # only one paren
        if (closeParen == -1 or openParen == -1) or (closeParen < openParen):
            print "Invalid rhyme scheme! Not all parentheses closed"
            return False
        if (closeParen - openParen <=1):
            print "Invalid rhyme scheme! Parenthesis with nothing inside."
            return False
        form = form[:openParen] + form[closeParen+1:]
    return True

# Check number of lines!
# Only works if there is a single parenthesized segment
def checkLines(poemScheme, pattern):
    linesBool = True
    noParenTotal = 0
    listOfMods = list()

    #no parens
    if pattern.find('(') == -1:
        linesBool = (len(poemScheme) == len(pattern))
    
    #at least one paren
    else:
        while not (not pattern):

            # run into paren
            if pattern[0] == '(':
                closeParen = pattern.find(')')
                modVal = len(pattern[1:closeParen])
                listOfMods.append(modVal)
                pattern = pattern[closeParen+1:]
            else:
                firstParen = pattern.find('(')
                noParenTotal = noParenTotal + firstParen
                pattern = pattern[firstParen:]
                
        numLinesforMod = (len(poemScheme) - noParenTotal)
        for val in listOfMods:
            numLinesforMod = numLinesforMod % val

        linesBool = (numLinesforMod == 0)
    if linesBool:
        print "Correct number of lines for specified rhyme scheme."
        return True
    else:
        print "Incorrect number of lines for specified rhyme scheme!"
        return False

def twoWordsRhyme(word1, word2):
    firstWordWords = rhymeListFromWord(word1, 1000)
    
    secondWordWords = rhymeListFromWord(word2, 1000)
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

def rhymeListFromWord(word, count):
    wordStr = rhymesFromWord(word, count)
    wordJSONThing = json.loads(wordStr)
    return map(lambda k: k["word"], wordJSONThing)

def rhymeListFromWordShort(word):
    return rhymeListFromWord(word, 20)

def createScheme(schemeDict, words):
    ret = ""
    schemeChar = 'a'
    count = 0

    for word in words:
        count += 1
        print "Checking rhymes for line number " + str(count) 
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
    return (ret, schemeDict)

###############
### Parser
###
### takes the pattern as parsed by schemehandler, and checks that it matches against what it should
###############
def schemeParser(schemeDict, pattern, parsedPattern, lastWordsList):
    # if not checkSameLetters(pattern, parsedPattern):
    #     return schemeDict
    
    patternCopy = pattern
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
                rhymeList = ', '.join(rhymeListFromWordShort(schemeDict[pattern[0]]))
                didNotMatchScheme(parsedPatternIndex, lastWordsList, pattern, schemeDict, rhymeList)
                return schemeDict
    if parsedPattern:
        someLinesNotParsed(parsedPatternIndex, lastWordsList, schemeDict)
        return schemeDict

    if (not pattern) and (not parsedPattern):
        print "The poem matches the scheme! Great work!"
        return schemeDict

# a function that checks if the number of unique letters in the pattern matches the scheme.
# this is a good speed boost but makes it harder to provide good feedback.
# it's currently commented out in schemeParser, to show how it would be used if added back in 
def checkSameLetters(pattern, parsedPattern):
    sortedPattern = ''.join(sorted(pattern))
    sortedParsedPattern = ''.join(sorted(parsedPattern))

    if sortedPattern[-1] == sortedParsedPattern[-1]:
        return True
    else:
        notSameLetters(pattern, parsedPattern)

