### input: filename (of a text file)
### output: list of lines in the text file
### This is important because all poem manipulation will work off of this form
def filenameToLines(filename):
    lines = open(filename, 'r').read().splitlines()
    return lines

### input: list of lines
### output: last word of every line
### This is important for rhymechecking, checking against a scheme, etc.
def lastWords(lines):
    ret = []
    for line in lines:
        line = line.split()
        ret.append(line[-1])
    return ret