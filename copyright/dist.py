from nltk.tokenize import word_tokenize
from gensim import corpora, models, similarities

class Dist:
    def __init__(self, temp):
        self.names = [name for name in temp]
        texts_tokenized = [[word.lower() for word in word_tokenize(
            temp[name])] for name in self.names]
        self.dictionary = corpora.Dictionary(texts_tokenized)
        corpus = [self.dictionary.doc2bow(d) for d in texts_tokenized]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        self.lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=10)
        self.index = similarities.MatrixSimilarity(self.lsi[corpus])

    def license(self, text):
        lic_tokenized = [word.lower() for word in word_tokenize(text)]
        curr_bow = self.dictionary.doc2bow(lic_tokenized)
        curr_lsi = self.lsi[curr_bow]
        sims = self.index[curr_lsi]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        if sort_sims[0][1] >= 0.95:
            return self.names[sort_sims[0][0]]
        return 'unknown'