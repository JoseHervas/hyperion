# -*- coding: utf-8 -*-
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import unidecode
from sys import argv


def preprocess(statementA, statementB):

    punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))
    lemmatizer = WordNetLemmatizer()
    stopWords = set(stopwords.words('spanish'))

    # Remove accents
    statementA = unidecode.unidecode(statementA.text)
    statementB = unidecode.unidecode(statementB.text)

    # Make both strings lowercase
    statementA = statementA.lower()
    statementB = statementB.lower()

    # Remove punctuation from each string
    statementA = statementA.translate(punctuation_table)
    statementB = statementB.translate(punctuation_table)

    # Tokenize sentences
    pos_a = pos_tag(word_tokenize(statementA, language='spanish'))
    pos_b = pos_tag(word_tokenize(statementB, language='spanish'))

    def treebank_to_wordnet(pos):
        """
        Convert Treebank part-of-speech tags to Wordnet part-of-speech tags.
        * https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        * http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
        """
        data_map = {
            'NN': wordnet.NOUN,
            'JJ': wordnet.ADJ,
            'VB': wordnet.VERB,
            'RB': wordnet.ADV
        }
        return data_map.get(pos[1]) if data_map.get(pos[1]) else wordnet.NOUN

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

    ratio = numerator / denominator

    if ("-dev" in argv):
        print("================")
        print(lemma_a)
        print(lemma_b)
        print("Numerator: " + str(numerator))
        print("Denominator: " + str(denominator))
        print("Ratio: " + str(ratio))

    return ratio
