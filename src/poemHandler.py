import re

### input: filename (of a text file)
### output: list of lines in the text file
### This is important because all poem manipulation will work off of this form
def filenameToLines(filename):
    lines = open(filename, 'r').read().splitlines()
    return lines

### input: list of lines
### output: last word of every line, with all non-alphas removed (e.g. apostrophes)
### This is important for rhymechecking, checking against a scheme, etc.
def lastWords(lines):
    ret = []
    for line in lines:
        if line != "":
            line = line.split()
            word = line[-1]
            #remove all non alphas from word
            regex = re.compile('[^a-zA-Z]')
            word = regex.sub('', word)
            ret.append(word)
    return ret