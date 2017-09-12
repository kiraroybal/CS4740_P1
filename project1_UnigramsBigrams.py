from collections import defaultdict
from pprint import pprint
import pandas as pd


# create bigram table
def store_counts(filename):
    text_file = open(filename, 'r')
    lines = text_file.readlines()
    types = defaultdict(lambda: defaultdict(int))

    for line in lines:
        #Standardize the contractions ('t is a separate word)
        tokens = line.replace(" n't", "n 't")
        #Get rid of hyphens
        tokens = line.replace('-', ' ')
        tokens = ['<s>'] + line.split() + ['</s>']

        count = len(tokens)
        for i in range(count-1):
            # treat upper and lower case words the same
            word1 = tokens[i].lower()
            word2 = tokens[i+1].lower()
            types[word1][word2] += 1

    # convert dictionary to table
    table = pd.DataFrame(types).T.fillna(0).applymap(lambda x: int(x))
    # add totals
    table['SUM'] = table.sum(axis=1)
    return table

# return the unigram for a given word, with a given table of counts
def unigram(word, table):
    try:
        return table.loc[word, 'SUM']
    except KeyError:
        print "This word doesn't exist in the corpus."

# return the bigram P(word2|word1) for the given table of counts
def bigram(word1, word2, table):
    try:
        return float(table.loc[word1, word2])/float(unigram(word1, table))
    except KeyError:
        print "Either word1 or word2 doesn't exist in the corpus"

#create sum list
def sumList(table):
    sums = table["SUM"]
    characters = sums.index.tolist()

    wordprob = []

    for i in range(0, sums.count-1):
        currentcount = sums[i]
        currentword = characters[i]
        for i in range(1, currentcount):
            wordprob.append(currentword)

    return wordprop

#create random unigram sentence
def rsgUnigram(table):
    endgram = False
    wordlist = sumList(table)
    sentence = wordlist[randrange(0, len(wordlist)-1)]
    while(!endgram):
        currentindex = randrange(0, len(wordlist)-1)
        currentword = wordlist[currentindex]
        sentence = sentence + " " + currentword

        if("currentword is an endgram"):
            endgram = True

    return sentence

def bigram_sentence_generator(counts):
    counts = counts.drop('SUM', axis=1)
    sentence = ''
    token = '<s>'
    while (token != '</s>'):
        row = counts.loc[token]  # get counts based on previous token
        token_list = []  # create a list of tokens based on counts
        for label, value in row.iteritems():
            token_list.extend([label] * value)
        rd_idx = randint(0, len(token_list) - 1)  # pick random index
        token = token_list[rd_idx]  # get corresponding token
        sentence += ' ' + token
    return sentence.split('</s>')[0].strip()



if __name__== "__main__":
    pos_counts = store_counts('pos.txt')
    neg_counts = store_counts('neg.txt')
