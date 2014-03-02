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
        words.append(CONST_TEENS[num - 10])
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

#converts a date (i.e. the 31 in "March 31" or 3/4) to spoken words, not compatible with years
def date_to_words(date):
    #M/D format
    if "/" in date :
        return [date]
    else:
        date = int(date)
        if date >= 10 and date < 20 :
            if date == 12 :
                return ['twelfth']
            else:
                return [CONST_TEENS[date - 10] + "th"]
        elif (date % 10) == 0 :
            tens_digit = date // 10
            return [CONST_TIES[tens_digit - 2][:-1] + "ieth"]
        elif date < 10 :
            return [CONST_ORDINALS[date - 1]]
        else:
            tens_digit = date // 10
            ones_digit = date % 10
            return [CONST_TIES[tens_digit - 2], CONST_ORDINALS[ones_digit - 1]]

#end of function

#transforms year into spoken words
#assumes 999 < year < 10000
def year_to_words(year):
    year = int(year)

    if year % 1000 == 0 :
        return int_to_words(str(year), [])

    #used paired format (i.e. 1750 => seventeen fifty)
    #except in cases like 2006 
    #accounts for the addition of "oh" in years like 1906
    first_pair = year // 100
    second_pair = year % 100
    if second_pair < 10 :
        if first_pair % 10 != 0 :
            return int_to_words(str(first_pair), []) + ["oh"] + int_to_words(str(second_pair), [])
        else: 
            return int_to_words(str(first_pair * 100), []) + int_to_words(str(second_pair), [])
    else:
        return int_to_words(str(first_pair), []) + int_to_words(str(second_pair), [])

#end of function

#return True if num is an int, False if not
def isint(num):
    try:
        intnum = int(num)
        return True
    except ValueError:
        return False

#end of function

#converst number to series of spoken digits
def digits_to_words(num):
    digits = []
    for d in list(num) :
        digit = int(d)
        digits.append(CONST_DIGITS[digit - 1])
    return digits

#converts a float (assumed to have a decimal portion)
def float_to_words(num):
    dec_point = num.index('.')
    intpart = num[:dec_point]
    decpart = num[dec_point + 1 :]
    return int_to_words(intpart, []) + ["point"] + digits_to_words(decpart)

#return True if num is a float, False if not
def isfloat(num):
    try:
        floatnum = float(num)
        return True
    except ValueError:
        return False

#end of function

#converts num to spoken words using int_to_words and float_to_words
def num_to_words(num):
    if isint(num) :
        return int_to_words(num, [])
    elif isfloat(num) :
        return float_to_words(num)
    else:
        return [num]

#end of function

#converts abbreviation to how it is spoken
def abbreviation_to_words(abbr):
    abbr = abbr.lower()
    #abbreviations that are pronounced as series of letters
    as_letters = ['dvd', 'un', 'pc', 'ibm', 'am', 'pm']
    #abbreviations spoken as an actual word (shown for example)
    as_word = ['nasa', 'ikea', 'unicef']
    expand = { 'mrs': ['missus'], 'ms': ['miss'], 'mr': ['mister'],
                'am': ['ay', 'em'], 'pm': ['pee', 'em'],
                'etc': ['et', 'cetera'],
                'adj.': ['adjective'], 'adjs.': ['adjectives'],
                'jan': ['january'], 'feb': ['february'], 'mar': ['march'],
                'apr': ['april'], 'aug': ['august'], 'sept': ['september'],
                'nov': ['november'], 'dec': ['december']}
    if "." in abbr :
        abbr = abbr.replace(".", "")
        print(abbr)
        if abbr in expand.keys() :
            return expand[abbr]
        else:
            return [abbr]
    if abbr in as_letters :
        return list(abbr)
        return [abbr]
    return [abbr]

#end of function

#converts time in format HH:MM to spoken words, i.e. 11:45 to eleven forty five
def time_to_words(time):
    first_pair = time[:-3]
    second_pair = time[-2:]
    if isint(first_pair) and isint(second_pair) :
        sp_int = int(second_pair)
        if sp_int < 10 :
            if sp_int == 0 :
                return int_to_words(first_pair, []) + ["o'clock"]
            else:
                return int_to_words(first_pair, []) + ['oh'] + int_to_words(second_pair, [])
        else:
            return int_to_words(first_pair, []) + int_to_words(second_pair, [])
    else:
        return [time]

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

    #if a word is in all caps, treat it as an abbreviation
    if raw_word.isupper() :
        return abbreviation_to_words(raw_word)
    
    #convert to lowercase
    raw_word = raw_word.lower()

    #normalizes integers, checking to see if a number is date or year
    if isint(raw_word) :
        num = int(raw_word) 
        #checks if num is referring to a date
        if not has_comma and num <= 31 and num > 0 :
            if index > 0 :
                prev_word = words[index - 1].lower()
                if prev_word in CONST_MONTHS :
                    return date_to_words(raw_word)
            if index < len(words) - 2 :
                next_word = words[index + 1].lower()
                nextN_word = words[index + 2].lower()
                if next_word == "of" and nextN_word in CONST_MONTHS :
                    return date_to_words(raw_word)
        #checks if num is referring to a year
        elif not has_comma and num > 1500 and num < 2100 :
            return year_to_words(raw_word)
        return int_to_words(raw_word, [])
    #normalizes floats (i.e. 34.5)
    elif isfloat(raw_word) :
        return float_to_words(raw_word)
    #changes $ format to "dollars"
    elif raw_word[0] == "$" :
        num = raw_word[1:]
        numpart = num_to_words(num)
        if index < len(words) - 1 :
            next_word = words[index + 1].lower()
            if next_word in ['hundred', 'thousand', 'million', 'billion', 'trillion'] :
                words.pop(index + 1)
                return numpart + [next_word, "dollars"]
        else:
            return numpart + ["dollars"]
    #if the word has a dot at the end, check if it's an abbreviation
    elif "." in raw_word :
        return abbreviation_to_words(raw_word)
    #if the word has a colon in the middle, check if it's referring to time
    elif ":" in raw_word :
        return time_to_words(raw_word)
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







