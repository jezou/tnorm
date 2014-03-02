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
    try:
        line = raw_input()
    except EOFError:
        print("EOF Reached - Programming terminating")
        break
    
    #checks for empty line
    if not line or len(line) == 0:
        print("Program terminating")
        break
    else:
        #tokenize by spaces
        words = line.split(" ")
        #loops through all "words" in words
        for index, word in enumerate(words) :
            choose(words, index)

#end of program














