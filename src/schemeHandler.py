import collections
import json

from APIFunctions import rhymesFromWord

# Check if the form contains appropriate parentheticals and only alphanumerics otherwise
def checkValidForm(form):
    while not (not form):
        closeParen = form.find(")")
        openParen = form.find("(")
        # no parens
        if (closeParen == -1 and openParen == -1):
            return True
        # only one paren
        if (closeParen == -1 or openParen == -1) or (closeParen > openParen):
            print "Invalid form! Not all parentheses closed"
            return False
        if (closeParen - openParen <=1):
            print "Invalid form! Parenthesis with nothing inside."
            return False
        form = form[:openParen] + form[closeParen+1:]

# Check number of lines!
# Only works if there is a single parenthesized segment
def checkLines(poemScheme, pattern):
    linesBool = True
    noParenTotal = 0
    listOfMods = list()

    while not (not pattern):
        # run into paren
        if pattern[0] == '(':
            closeParen = pattern.find(")")
            modVal = len(pattern[1:closeParen])
            listOfMods.append(modVal)
            pattern = pattern[closeParen+1:]
        else:
            firstParen = pattern.find("(")
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
        print count 
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
    if not checkSameLetters(pattern, parsedPattern):
        return schemeDict
    
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
                didNotMatchScheme(parsedPatternIndex, lastWordsList, pattern, schemeDict)
                return schemeDict
    if parsedPattern:
        someLinesNotParsed(parsedPatternIndex, lastWordsList, schemeDict)
        return schemeDict

    if (not pattern) and (not parsedPattern):
        print "The poem matches the scheme! Great work!"
        return schemeDict

def checkSameLetters(pattern, parsedPattern):
    sortedPattern = ''.join(sorted(pattern))
    sortedParsedPattern = ''.join(sorted(parsedPattern))

    if sortedPattern[-1] == sortedParsedPattern[-1]:
        return True
    else:
        notSameLetters(pattern, sortedParsedPattern)

#### ERROR MESSAGES ####
def didNotMatchScheme(parsedPatternIndex, lastWordsList, pattern, schemeDict):
    print "Poem did not match specified scheme!"
    print "Incorrect line is line " + str(parsedPatternIndex + 1) + ", with last word: " + lastWordsList[parsedPatternIndex]
    print "The scheme expects the word to match the '" + pattern[0] + "' rhyme pattern"
    print "As such, the last word on the line should rhyme with " + schemeDict[pattern[0]]
    print "Here are some rhyme suggestions that match with that word: " 
    print ', '.join(rhymeListFromWordShort(schemeDict[pattern[0]]))
    print "Current letter assignments:", json.dumps(schemeDict, indent=4)

def notSameLetters(pattern, sortedParsedPattern):
    print "Poem cannot match specified scheme! The poem and scheme do not expect the same number of unique rhymes!"
    print "The expected rhyme scheme is " + pattern + ", and the poem was determined to have scheme " + sortedParsedPattern

def someLinesNotParsed(parsedPatternIndex, lastWordsList, schemeDict):
    print "Poem did not match specified scheme! Some lines not parsed!"
    print "The first line not parsed is line " + str(parsedPatternIndex + 1) + ", with last word: " + lastWordsList[parsedPatternIndex]
    print "the current letter assignments are: ", json.dumps(schemeDict, indent=4)
