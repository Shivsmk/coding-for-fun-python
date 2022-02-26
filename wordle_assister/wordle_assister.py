# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 20:19:32 2022

@author: Shiv Muthukumar
@description: Based on the first guess, the program will narrow down the list
of words that can represent the solution to the wordle puzzle.
@version: 2
"""

"""
THE PROGRAM BELOW ASSUMES YOU HAVE A TXT FILE CONTAINING MOST (IF NOT ALL) OF
THE 5-LETTER WORDS IN THE ENGLISH DICTIONARY. IF YOU DON'T, YOU CAN RUN THE 
BELOW COMMENTED PEICE OF CODE TO GENERATE THE TXT FILE. 
IT GENERATES ALL THE POSSIBLE COMBINATION OF 5-LETTER WORDS AND CHECKS AGAINST
A DICTIONARY PACKAGE. IF THE WORD FORMED IS A GENUINE WORD, IT IS ADDED TO THE
TEXT FILE.
"""
# =============================================================================
# from itertools import product
# from string import ascii_lowercase
# import enchant
# en = enchant.Dict("en_US")
# 
# def generate_n_letter_words_into_file(n):
#     with open("lettercombo.txt", 'w') as text_file:
#         for i in product(ascii_lowercase, repeat = n):
#             word = ''.join(i)
#             if en.check(word):
#                 text_file.write("%s\n" % word)
# =============================================================================

# ADDS WORD TO THE LIST OF WORDS IF THE CONDITION IS MET
def word_filter(wordslist, word, condition, charlist):
    if condition == 'include':
        if word_condition_check(word, 'include', charlist):
            wordslist.append(word)
    if condition == 'exclude':
        if word_condition_check(word, 'exclude', charlist):
            wordslist.append(word)
    if condition == 'exact':
        if word_condition_check(word, 'exact', charlist):
            wordslist.append(word)
    if condition == 'forget':
        if not word_condition_check(word, 'forget', charlist):
            wordslist.append(word)
    return wordslist

# CREATES A LIST OF WORDS FROM THE TXT FILE THAT SATISFIES THE CONDITION
def get_words_from_file_into_list(filename, condition, charlist):
    wordslist = []
    with open(filename) as text_file:
        for line in text_file:
            line = line.strip()
            wordslist = word_filter(wordslist, line, condition, charlist)
    return wordslist

# REDUCES THE EXISTING LIST OF WORDS BASED ON CONDITIONS
def narrow_wordslist(wordslist, condition, charlist):
    temp_words_list = []
    for word in wordslist:
        temp_words_list = word_filter(temp_words_list, word, condition, charlist)
    return temp_words_list

# DECIDES IF A WORD ADHERES TO THE REQUIRED CONDITION AND RETURNS TRUE/FALSE
# INCLUDE - ENSURES THE WORD CONTAINS ALL THE REQURIED LETTERS
# EXCLUDE - ENSURES THE WORD DOES NOT CONTAIN ALL THE NOT REQUIRED LETTERS
# EXACT - ENSURES THE WORD CONTAINS THE REQUIRED LETTER IN THE EXACT LOCATION
# FORGET - ENSURES THE WORD DOES NOT CONTAIN AN INCLUDED LETTER IN THE PREVIOUS KNOWN LOCATION
def word_condition_check(word, condition, charlist):
    if condition == 'include':
        return all(e in word for e in charlist)
    if condition == 'exclude':
        return not any(e in word for e in charlist)
    if condition == 'exact':
        i = 0
        while i < len(word):
            if charlist[i] != '*':
                if word[i] != charlist[i]:
                    return False
            i+=1
        return True
    if condition == 'forget':
        for w in charlist:
            if word[int(w[0])] == w[1]:
                return True
        return False

# TAKES THE INPUT AND DECODES IT INTO THE RELEVANT LISTS
# 0? -> LETTER DOES NOT EXIST IN THE WORD
# 1? -> LETTER EXISTS BUT IS IN THE INCORRECT LOCATION IN THE WORD
# 2? -> LETTER IS IN THE CORRECT LOCATION IN THE WORD        
def decode_input(itext, include_list=[], forget_list=[], exclude_list=[], exact_list=['*','*','*','*','*']):
    i=0
    while i < len(itext):
        if itext[i] == '0': # Case of Not There
            exclude_list.append(itext[i+1])
            i+=1
        elif itext[i] == '1': # Case of Incorrect Position
            include_list.append(itext[i+1])
            forget_list.append(str(int(i/2))+itext[i+1])
            i+=1
        elif itext[i] == '2': # Case of Correct Position
            exact_list[int(i/2)] = itext[i+1]
            i+=1
        i+=1
    return (include_list, forget_list, exclude_list, exact_list)

# TAKES THE FILTERED WORD LIST AND GENERATES A FREQUENCY LIST OF CHARACTERS
# OUTPUTS A LIST OF TUPLES WITH THE FREQUENCY COUNT IN DESCENDING ORDER
def frequency_of_letters(wordslist):
    frequency_list = {}
    for word in wordslist:
        for i in word:
            if i in frequency_list:
                frequency_list[i] += 1
            else:
                frequency_list[i] = 1
    return sorted(frequency_list.items(), key=lambda x:x[1], reverse=True)

# LOGIC FOR A SINGLE ITERATION - FOR THE SECOND, THIRD, AND FOURTH ITERATIONS
# TAKES THE INPUT, DECODES IT INTO THE REQUIRED LIST
# FILTERS IT DOWN BY EXCLUDING ALL THE WORDS THAT CONTAIN NOT REQURIED LETTERS
# THEN FILTERS DOWN BY ENSURING IT INCLUDES ALL THE REQURIED LETTERS
# THEN FILTERS DOWN BY ENSURING THE WORD DOES NOT CONTAIN AN INCLUDED LETTER IN THE PREVIOUS KNOWN LOCATION
# FINALLY FILTERS DOWN BY ENSURING THE WORDS CONTAIN THE LETTERS IN THE EXACT SPOT
# PRINTS THE LIST OF WORDS FOR THE USER TO CHOOSE FROM
# PRINTS THE FREQUENCY OF LETTERS OCCURING IN THE ABOVE LIST
def single_logic_cycle(wordslist, include_list, forget_list, exclude_list, exact_list):
    guess = input("Guess: ")
    include_list, forget_list, exclude_list, exact_list = decode_input(guess, include_list, forget_list, exclude_list, exact_list)
    wordslist = narrow_wordslist(wordslist, 'exclude', exclude_list)
    wordslist = narrow_wordslist(wordslist, 'include', include_list)
    wordslist = narrow_wordslist(wordslist, 'forget', forget_list)
    wordslist = narrow_wordslist(wordslist, 'exact', exact_list)
    print("\nList of possible words:")
    print(wordslist)
    print("\nFrequency count of occurring characters:")
    print(frequency_of_letters(wordslist))
    return wordslist

def main():
    # FIRST ITERATION
    # TAKE THE FIRST GUESSED RESULT FROM WORDLE
    guess = input("Initial Guess: ")
    # DECODE THE INTPUT
    include_list, forget_list, exclude_list, exact_list = decode_input(guess)
    # PERFORM THE 4 FILTERATION ONE BY ONE IN ORDER
    wordslist = get_words_from_file_into_list('lettercombo.txt', 'exclude', exclude_list)
    wordslist = narrow_wordslist(wordslist, 'include', include_list)
    wordslist = narrow_wordslist(wordslist, 'forget', forget_list)
    wordslist = narrow_wordslist(wordslist, 'exact', exact_list)
    print("\nList of possible words:")
    print(wordslist)
    print("\nFrequency count of occurring characters:")
    print(frequency_of_letters(wordslist))
    # FOR SUBSEQUENT INTERATIONS - USE THE PACKAGED FUNCTION
    # SECOND ITERATION
    wordslist = single_logic_cycle(wordslist, include_list, forget_list, exclude_list, exact_list)
    # THIRD ITERATION
    wordslist = single_logic_cycle(wordslist, include_list, forget_list, exclude_list, exact_list)
    # FOURTH ITERATION
    wordslist = single_logic_cycle(wordslist, include_list, forget_list, exclude_list, exact_list)
    print("You should be able to guess the word by now. If not, blame on the bad first guess!")

if __name__ == "__main__":
    main()

