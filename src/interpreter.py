import collections
import json

from poemHandler import lastWords, filenameToLines
from schemeHandler import createScheme, rhymeListFromWordShort, checkLines, schemeParser, checkValidForm


class Interpreter(object):
    def __init__(self):
        self.schemeDict = collections.OrderedDict()
        self.formDict = collections.OrderedDict()

    ###############
    ### MAIN functionality
    ###############
    ## for checking a pattern that is input manually by the user
    def checkPattern(self, filename, pattern):
        # take the filename and open it into lines, then last words of lines
        lines = filenameToLines(filename)
        lastWordsList = lastWords(lines)

        # check lines!!
        if not checkLines(lastWordsList, pattern):
            return 

        # use the last words to create a scheme
        createSchemeReturn = createScheme(self.schemeDict, lastWordsList)
        
        # get the scheme of the poem, as well as the now updated dictionary,
        # from the scheme helper
        poemScheme = createSchemeReturn[0]
        self.schemeDict = createSchemeReturn[1]

        # parse through and determine if the 
        self.schemeDict = schemeParser(self.schemeDict, pattern, poemScheme, lastWordsList)
        return ''

    def checkForm(self, filename, formName):
        pattern = self.formDict[formName]
        self.checkPattern(filename, pattern)

    # Add a scheme to our formDict!
    def addForm(self, form, formName):
        if checkValidForm(form):
            self.formDict[formName] = form
            print "Added form " + form + " with name " + formName
        else:
            print "Could not add form."

if __name__ == '__main__':
    interpreter = Interpreter()
    # print "checking how now brown cow on aaba"
    # print(interpreter.checkPattern("tmp.txt", r'a(ab)(ab)'))
    interpreter.addForm(r'ababcdcdefefgg', 'sonnet')
    # print "checking a sonnet is a sonnet"
    # print(interpreter.checkForm("sonnet.txt", 'sonnet'))
