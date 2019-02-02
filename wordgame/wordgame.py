# wordgame in python

import pandas as pd
import random
import re

# sort letters in a string
def ano_sort(x):
    x = list(x)
    x = sorted(x)
    x = ''.join(x)
    return(x)


# get unique letters in a string
def ano_unique(x):
    #x = sorted(list(set(test_str)))
    x = set(x)
    x = list(x)
    x = sorted(x)
    x = ''.join(x)
    return(x)


# test if a string exist as a substring of a longer string
def ano_subset(ano, sub):
    x = set(ano).issubset(sub)
    return(x)


# shuffle the letters
def ano_shuffler(word, letter):
    #x = list(word)
    x = list(set(word) - set(letter))
    x = random.sample(x, len(x))
    x = letter + ''.join(x)
    return(x)


# update guess
def update_guess(df_derivatives, x):
    if x in pd.Series(list(df_derivatives['word'])).unique():
        df_derivatives.guessed[df_derivatives['word'] == x] = True
    return df_derivatives


# shuffle order of letters, keeping base letter first
def shuffle():
    x = (ano_shuffler(word7, base_letter))
    x = ' '.join(x)
    return(x)


# print unguessed words
def give_up():
    x = df_derivatives[['word', 'bonus']][df_derivatives['guessed'] == False]
    x = x.assign(out=(x.word + '*').where(x.bonus == True, x.word))
    x = x[['out']]
    print(x.to_string(justify='start', index=False))


# options for displaying current game play results
def results(x):
    tot_pts = df_derivatives['points'].sum()
    pts = df_derivatives['points'][df_derivatives['guessed'] == True].sum()
    tot_wrds = len(df_derivatives)
    wrds = len(df_derivatives['points'][df_derivatives['guessed'] == True])
    if x == 'points':
        print(pts)
    elif x == 'word_count':
        print(wrds)
    elif x == 'percent_words':
        print(round(wrds / tot_wrds * 100, 1))
    elif x == 'percent_points':
        print(round(pts / tot_pts * 100, 1))
    elif x == 'words':
        print(df_derivatives['word'][df_derivatives['guessed'] == True].to_string(index=False))
    else:
        print("Please use 'points', 'word_count', 'percent_words', 'percent_points', or 'words' to get current results")


# game play
def wordgame(x):
    x = x.lower()
    if len(x) < 4:
        return('Words must contain at least 4 letters')
    elif base_letter not in x:
        return("Sorry, the word must contain the letter '" + base_letter + "'.")
    elif x in pd.Series(list(df_derivatives[df_derivatives['guessed'] == True]['word'])).unique():
        return("Sorry, '" + x + "' has already been guessed.")
    elif x in pd.Series(list(df_derivatives['word'])).unique():
        pts = df_derivatives['points'][df_derivatives['word'] == x].values[0] 
        update_guess(df_derivatives, x)
        if not df_derivatives[(df_derivatives['chars_unique'] >= 7) & (df_derivatives['word'] == x)].empty:
            return('Pangram! All seven letters - 2x bonus points! +' + str(pts))
        else:
            return('Yeehaw! +' + str(pts)) # + ' points!'
    else:
        return("Sorry, '" + x + "' does not work.")


### data
# get the word list 
words_url = 'http://norvig.com/ngrams/TWL06.txt'
df_words = pd.read_csv(words_url, header=None, names=['word'])
#df_words = pd.read_csv('/Users/stuartharty/Documents/data/df_words.csv')

df_words['word'] = df_words['word'].str.lower()

df_words['chars_total'] = df_words['word'].str.count('[a-z]')

df_words = df_words[df_words['chars_total'] > 3]

df_words['ano'] = df_words.apply(lambda row: ano_sort(row['word']), axis=1)
df_words['ano_unique'] = df_words.apply(lambda row: ano_unique(row['ano']), axis=1)
df_words['chars_unique'] = df_words['ano_unique'].str.count('[a-z]')

df_words = df_words[df_words['chars_unique'] > 1]

df_words['vowels'] = df_words['ano'].str.replace('[^aeiouy]','', regex=True)
df_words['vowels_unique'] = df_words.apply(lambda row: ano_unique(row['vowels']), axis=1)

df_words7 = df_words[(df_words['chars_total'] == 7) & (df_words['chars_unique'] == 7)]
df_words7 = df_words7[df_words7['vowels_unique'].str.count('[a-z]') == 2]



def start_game():
    global word7
    global df_derivatives
    global base_letter
    global word_non_vowel

    # find words that can be used for the base
    word7 = df_words7['ano'].sample(n=1).values[0]

    # define a base letter
    word_non_vowel = re.sub(r'[aeiouy]', '', word7)
    base_letter = random.choice(list(word_non_vowel))

    df_words['sub_word_chars'] = df_words.apply(lambda row: sum(elem in set(word7)  for elem in set(row['ano_unique'])), axis=1)
    df_derivatives = df_words[df_words['sub_word_chars'] == df_words['chars_unique']].copy()
    df_derivatives = df_derivatives[df_derivatives['ano_unique'].str.contains(base_letter)].copy()
    df_derivatives['points'] = df_derivatives['word'].str.count('[a-z]') - 3
    df_derivatives['bonus'] = df_derivatives['chars_unique'] >= 7

    df_derivatives.loc[df_derivatives['bonus'] == True, 'points'] = df_derivatives['points'] * 2
    df_derivatives['guessed'] = False 
    print(shuffle())



def restart():
    give_up()
    start_game()
    



### game play ###
# start_game()

# wordgame('dabbing') 

# shuffle()

# results('points')
# results('word_count')
# results('percent_words')
# results('percent_points')
# results('nothing')
# results('words')

# give_up()


