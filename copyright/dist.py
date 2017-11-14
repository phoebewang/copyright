import re
from nltk.tokenize import word_tokenize
from gensim import corpora, models, similarities

stopwords = ['*', '.', '[', ']', 'license', 'copyright', 'the', '(', ')', ';', 'is', 'are', 'of', 'for', 'and', 'file', 'under', '<', '>', 'this']

class Dist:
    def __init__(self, temp):
        self.names = [name for name in temp]
        texts_tokenized = [[word.lower() for word in word_tokenize(
            re.sub('[/\-_=,\'#`]', '', temp[name]))] for name in self.names]
        texts_filtered_stopwords = [[word for word in document if not word in stopwords] for document in texts_tokenized]
        self.texts_tokenized = texts_filtered_stopwords
        self.dictionary = corpora.Dictionary(texts_filtered_stopwords)
        corpus = [self.dictionary.doc2bow(d) for d in texts_filtered_stopwords]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        self.lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=10)
        self.index = similarities.MatrixSimilarity(self.lsi[corpus])

    def license(self, text):
        text = text.encode('ascii')
        text = re.sub('[/\-_=,\'#`]', '', text)
        lic_tokenized = [word.lower() for word in word_tokenize(re.sub('[/\-_=,\'#]', '', text))]
        lic_tokenized_stopwords = [word for word in lic_tokenized if not word in stopwords]
        curr_bow = self.dictionary.doc2bow(lic_tokenized_stopwords)
        curr_lsi = self.lsi[curr_bow]
        sims = self.index[curr_lsi]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        if sort_sims[0][1] >= 0.98:
            return self.names[sort_sims[0][0]]
        return 'unknown'