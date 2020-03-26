import math
import nltk
import numpy as np
from nltk import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
from operator import itemgetter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

nltk.download('punkt')

def textrank(sentences, top_n):
    S = build_similarity_matrix(sentences)
    sentence_ranking = pagerank(S)
    ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranking), key=lambda item: -item[1])]
    selected_sentences = sorted(ranked_sentence_indexes[:top_n])
    return selected_sentences


def pagerank(matrix, eps=0.0001, d=0.85):
    P = np.ones(len(matrix)) / len(matrix)
    while True:
        new_P = np.ones(len(matrix)) * (1 - d) / len(matrix) + d * matrix.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P


def sentence_similarity(sent1, sent2):
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for w in sent1:
        vector1[all_words.index(w)] += 1
        
    for w in sent2:
        vector2[all_words.index(w)] += 1
    
    return 1 - cosine_distance(vector1, vector2) 


def build_similarity_matrix(sentences):
    S = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue

            S[i][j] = sentence_similarity(sentences[i], sentences[j])

    # normalisasi matrix
    for i in range(len(S)):
        S[i] /= S[i].sum()
    
    return S


def get_summary(text):
    stemmer_factory = StemmerFactory()
    stemmer = stemmer_factory.create_stemmer()

    sw_factory = StopWordRemoverFactory()
    stopwords = sw_factory.get_stop_words()

    # sentence splitting
    st = sent_tokenize(text)
    # tokenizing
    arr = [word_tokenize(stemmer.stem(sent)) for sent in st]
    # stopword removal
    arr = [[j for j in i if j not in stopwords] for i in arr]

    # n = math.floor((25/100) * len(st)) # jumlah kalimat yang akan dihasilkan
    n = 15

    final_summ = []

    summary = itemgetter(*textrank(arr, n))(st)
    for sentence in summary:
        final_summ.append(sentence)

    #return (' '.join(final_summ))
    return final_summ