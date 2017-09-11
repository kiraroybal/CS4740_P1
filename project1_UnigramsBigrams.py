from collections import defaultdict
from pprint import pprint
import pandas as pd


# create bigram table
def store_counts(filename):
    text_file = open(filename, 'r')
    lines = text_file.readlines()
    types = defaultdict(lambda: defaultdict(int))

    for line in lines:
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



if __name__== "__main__":
    pos_counts = store_counts('pos.txt')
    neg_counts = store_counts('neg.txt')