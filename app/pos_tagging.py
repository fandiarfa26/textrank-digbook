# POS TAGGING

from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import TokenEmbeddings, WordEmbeddings,StackedEmbeddings, BertEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

def pos_tagging():

    corpus = NLPTaskDataFetcher.load_corpus(NLPTask.UD_INDONESIAN)
    tag_type = 'upos'
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

    embedding_types: List[TokenEmbeddings] = [ WordEmbeddings('id-crawl'), WordEmbeddings('id') ]

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

    tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

    trainer: ModelTrainer = ModelTrainer(tagger, corpus)
    trainer.train('resources/taggers/example-universal-pos', learning_rate=0.1, mini_batch_size=32, max_epochs=10)

    print ("Training Model for POS TAGGER, Complete!")