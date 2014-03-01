#utils.py - contains various functions used in text normalization (used in tnorm.py)
#Jefferson Zou

#some useful lists
CONST_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
CONST_ORDINALS = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
CONST_TEENS = ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
CONST_DIGITS = ['one','two','three','four','five','six','seven','eight','nine']
CONST_TIES = ['twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
#converts integers to how they are spoken (assumes num is an integer)                                                                          
#i.e. 42 => forty two                                                                                                 
#*this doesn't encompass how numbers are spoken in all contexts
def int_to_words(num, words):

    num = int(num)

    if num == 0 and not words :
        words.append('zero')
        return words
    if num < 10 :
        if num != 0 :
            words.append(CONST_DIGITS[num - 1])
        return words
    if num < 20 and num >= 10 :
        words.append(teens[num - 10])
        return words
    else:
        place = len(str(num))
        tens = 10 ** (place - 1)
        digit = num // tens
        pre = -1

        if place not in[2, 5, 6, 8, 9, 11, 12]:
            words.append(CONST_DIGITS[digit - 1])

        #deals with "ties", i.e. twenty, thirty, etc.
        if place == 2 :
            words.append(CONST_TIES[digit - 2])
        elif place == 3 : 
            words.append('hundred')
        elif place == 4 :
            words.append('thousand')
        elif place == 5 or place == 6:
            #finding "prefix" to the thousand, i.e. 10 thousand, 20 thousand, 40 thousand
            pre = num // 1000
            words = words + int_to_words(pre, [])
            words.append('thousand')
            pre = pre * 1000
        elif place == 7 :
            words.append('million')
        elif place == 8 or place == 9 :
            pre = num // 1000000
            words = words + int_to_words(pre, [])
            words.append('million')
            pre = pre * 1000000
        elif place == 10 :
            words.append('billion')
        elif place == 11 or place == 12 :
            pre = num // 1000000000
            words = words + int_to_words(pre, [])
            words.append('billion')
            pre = pre * 1000000000

        if pre == -1 :
            num = num - (tens * digit)
        else:
            num = num - pre

        return int_to_words(num, words)

#end of function

#converts a date (i.e. the 31 in "March 31" or 3/4) to words, not compatible with years
def date_to_words(date):
    #M/D format
    if "/" in date :
        return date
    else:
        date = int(date)
        #error checking for a date of 0
        if date == 0 :
            return date
        #error checking for date > 31
        if date > 31 :
            return int_to_words(date)
        elif date >= 10 and date < 20 :
            return [CONST_TEENS[date - 10] + "th"]
        elif (date % 10) == 0 :
            tens_digit = date // 10
            return [CONST_TIES[tens_digit - 2][:-1] + "ieth"]
        else:
            tens_digit = date // 10
            ones_digit = date % 10
            return [CONST_TIES[tens_digit - 2], CONST_ORDINALS[ones_digit - 1]]

#end of function

#return True if num is an int, False if not
def isint(num):
    try:
        intnum = int(num)
        return True
    except ValueError:
        return False

#end of function

#normalizes non-standard words
def convertNSW(words, index):

    raw_word = words[index]

    #checks for and removes commas
    if "," in raw_word :
        has_comma = True
        raw_word = raw_word.replace(",", "")
    else:
        has_comma = False

    #normalizes integers, checking to see if a number is date or year
    if isint(raw_word) :
        if index > 0 :
            prev_word = words[index - 1]
            if prev_word in CONST_MONTHS :
                return date_to_words(raw_word)
        if index < len(words) - 2 :
            next_word = words[index + 1]
            nextN_word = words[index + 2]
            if next_word == "of" and nextN_word in CONST_MONTHS :
                return date_to_words(raw_word)
        return int_to_words(raw_word, [])
    #changes $ format to "dollars"
    elif raw_word[0] == "$" :
        num = raw_word[1:]
        print(num)
        intpart = int_to_words(num, [])
        if index < len(words) - 1 :
            next_word = words[index + 1]
            if next_word in ['hundred', 'thousand', 'million', 'billion', 'trillion'] :
                standardwords.pop(index + 1)
                return intpart + [next_word, "dollars"]
        else:
            return intpart + ["dollars"]
    else:
        return [raw_word]

#end of function

from nltk.corpus import cmudict
D = cmudict.dict()

#chooses the pronounciation to print
def choose(words, index):
    #normalizes non-standard words
    standardwords = convertNSW(words, index)
    for i, word in enumerate(standardwords) :
        #tries to get pronounciation, returns "<>" if one isn't found
        try:
            options = D[word]
            if len(options) == 1 :
                print(options[0])
            #tries to return a pronounciation based on context
            else:
                #chooses whether "a" is being used as an article - ['AH0'] (options[0]) - or a letter - ['EY1'] (options[1])
                if word == "a" :
                    if index > 0 :
                        prev_word = standardwords[i - 1]
                        if prev_word in ["the", "an"] :
                            print(options[1])
                            continue
                    if index < len(standardwords) - 1 :
                        next_word = standardwords[i + 1]
                        if next_word in ["to", "is", "isn't"] :
                            print(options[1])
                            continue
                    print(options[0])
                else:
                    print(options[0])
        except KeyError:
            print("<>")







