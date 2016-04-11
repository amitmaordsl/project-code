# import re
from interpreter import twoWordsRhyme
import collections

### input: list of last words from txt file
### output: string of characters designating rhyme scheme
# def createScheme(words):
#     ret = ""
#     schemeChar = 'a'
#     schemeDict = collections.OrderedDict()

#     for word in words:
#         # did the word match a rhyme higher in the poem
#         trackerHit = False
#         # char to be used if a match is found
#         trackerChar = ''
#         # iterate through the dictionary (in order), checking if the word rhymes with 
#         # any word already in the schema. if it does, 
#         for key, value in schemeDict.items():
#             if twoWordsRhyme(word, value):
#                 ret += key
#                 trackerHit = True
#                 trackerChar = key
#                 break
#         if not trackerHit:
#             ret += schemeChar
#             schemeDict[schemeChar] = word
#             schemeChar = chr(ord(schemeChar) + 1)
#         # print ret
#     return ret


#print createScheme(["how", "now", "brown", "frown", "poop", "scoop", "bow"])