# -*- coding: utf-8 -*-
from nltk import pos_tag
import nltk.data
import nltk
nltk.download('punkt')
tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
from nltk.corpus import wordnet, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string


def treebank_to_wordnet(pos):
    """
    Convert Treebank part-of-speech tags to Wordnet part-of-speech tags.
    * https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    * http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
    """
    data_map = {
        'N': wordnet.NOUN,
        'J': wordnet.ADJ,
        'V': wordnet.VERB,
        'R': wordnet.ADV
    }
    return data_map.get(pos[0])


def preprocess(statementA, statementB):

    punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))
    lemmatizer = WordNetLemmatizer()
    stopWords = set(stopwords.words('spanish'))

    # Make both strings lowercase
    statementA = statementA.text.lower()
    statementB = statementB.text.lower()

    # Remove punctuation from each string
    statementA = statementA.translate(punctuation_table)
    statementB = statementB.translate(punctuation_table)

    # Tokenize sentences
    pos_a = pos_tag(tokenizer.tokenize(statementA))
    pos_b = pos_tag(tokenizer.tokenize(statementB))

    lemma_a = [
        lemmatizer.lemmatize(
            token, treebank_to_wordnet(pos)
        ) for token, pos in pos_a if token not in stopWords
    ]
    lemma_b = [
        lemmatizer.lemmatize(
            token, treebank_to_wordnet(pos)
        ) for token, pos in pos_b if token not in stopWords
    ]

    return lemma_a, lemma_b

def jaccard(statementA, statementB):

    lemma_a, lemma_b = preprocess(statementA, statementB)

    # Calculate Jaccard similarity
    numerator = len(set(lemma_a).intersection(lemma_b))
    denominator = float(len(set(lemma_a).union(lemma_b)))
    print("Sentences: " + statementA.text + " / " + statementB.text)
    print(lemma_a)
    print(lemma_b)
    print("Numerator: " + str(numerator))
    print("Denominator: " + str(denominator))
    ratio = numerator / denominator

    return ratio
