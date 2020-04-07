import math
import nltk
import string
import numpy as np
from nltk import word_tokenize
from nltk.tag import CRFTagger
from operator import itemgetter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

def textrank(pos_tagged, top_n):
    processed_text = [x.split("__")[0] for x in pos_tagged if "__NN" in x or "__NNP" in x]
    vocabulary = list(dict.fromkeys(processed_text))
    
    S = build_weighted_edge(processed_text, vocabulary)
    score = pagerank(S)

    all_phrases = get_all_phrases(pos_tagged)

    score_phrase = []
    for x in all_phrases:
        temp_score = 0
        for y in x.split(" "):
            if y not in vocabulary:
                temp_score += 0
            else:
                temp_score += score[vocabulary.index(y)]
        
        temp_score = temp_score / len(x.split(" "))
        score_phrase.append(temp_score)
    
    sorted_index = np.flip(np.argsort(score_phrase), 0)

    final_keywords = []
    for i in range(0, top_n):
        final_keywords.append(all_phrases[sorted_index[i]])
    
    return final_keywords
    

def pagerank(matrix, eps=0.0001, d=0.85):
    P = np.ones(len(matrix)) / len(matrix)
    while True:
        new_P = np.ones(len(matrix)) * (1 - d) / len(matrix) + d * matrix.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P

def build_weighted_edge(processed_text, vocabulary, window_size=3):
    vocab_len = len(vocabulary)

    S = np.zeros((vocab_len, vocab_len))
    covered_cooccurrences = []

    for i in range(0, vocab_len):
        for j in range(0, vocab_len):
            if j == i:
                continue
            for window_start in range(0, (len(processed_text) - window_size + 1)):
                window_end = window_start + window_size
                window = processed_text[window_start:window_end]
                if (vocabulary[i] in window) and (vocabulary[j] in window):
                    index_of_i = window_start + window.index(vocabulary[i])
                    index_of_j = window_start + window.index(vocabulary[j])
                    if [index_of_i, index_of_j] not in covered_cooccurrences:
                        S[i][j] += 1/math.fabs(index_of_i - index_of_j)
                        covered_cooccurrences.append([index_of_i, index_of_j])
    
    for i in range(len(S)):
        S[i] /= S[i].sum()

    return S


def get_all_phrases(pos_tagged):
    sw_factory = StopWordRemoverFactory()
    stopwords = sw_factory.get_stop_words()
    
    phrases = []
    someword = [pos_tagged[0].split('__')[0]]
    for i in range(1,len(pos_tagged)):
        word = pos_tagged[i].split('__')[0]
        tag = pos_tagged[i].split('__')[1]
        prev_tag = pos_tagged[i-1].split('__')[1]
        if tag == prev_tag:
            someword.append(word)
        else:
            phrases.append(" ".join(someword))
            someword = [word]
    
    filtered = [i for i in phrases if i not in list(string.punctuation)]
    
    stopword_removed = [i for i in filtered if i not in stopwords]
    
    same_removed = list(dict.fromkeys(stopword_removed))
    
    non_propn_noun = [x.split("__")[0] for x in pos_tagged if "__NN" not in x and "__NNP" not in x]
    all_phrases = [i for i in same_removed if i not in non_propn_noun]

    return all_phrases

def pos_tagging(tokenized):
    ct = CRFTagger()
    ct.set_model_file('resources/taggers/all_indo_man_tag_corpus_model.crf.tagger')
    tagged = ct.tag_sents([tokenized])

    result = []
    for a in tagged:
        for i in a:
            result.append('__'.join(i))

    return result


def get_keywords(text):
    tokenized = word_tokenize(text.lower())
    pos_tagged = pos_tagging(tokenized)
    
    n = 10
    keywords = textrank(pos_tagged, n)

    return keywords