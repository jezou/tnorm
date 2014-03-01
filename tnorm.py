#tnorm.py - an exercise in text normalization
#Jefferson Zou
#transforms sentences into a sequence of phones
#uses the CMU Pronouncing Dictionary for dictionary lookup

from utils import *

#main body of program
#loop continues as long as line is not empty
line = "initial"
while(True):

    #reads in input line from user
    line = raw_input()
    
    #checks for empty line
    if not line :
        print("Program terminating")
        break
    else:
        #CMU only accepts lowercase
        line = line.lower()
        #tokenize by spaces
        words = line.split(" ")
        #loops through all "words" in words
        for index, word in enumerate(words) :
            choose(words, index)

#end of program














