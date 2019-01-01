import gensim
import warnings
from konlpy.tag import Mecab
from collections import Counter
from gensim import corpora
from gensim import models
from pyLDAvis import gensim as gensimvis
from pyLDAvis import display
from pyLDAvis import save_html
warnings.filterwarnings(action='ignore')


class NewsMining:

    def __init__(self, file, topic_num=40):
        self.news_file = file
        self.topic_num = topic_num

    def _extract_noun(self):
        mecab = Mecab()
        self.article_list = []
        with open(self.news_file, 'r') as file:
            for article in file:
                extracted_noun = mecab.nouns(article)
                self.article_list.append(extracted_noun)

    def _clean_text(self):
        article_num = 0
        for split_article in self.article_list:
            self.article_list[article_num] = list(filter(lambda x: len(x) >= 2, split_article))
            article_num += 1

    def _adapt_stopwords(self):
        """
        불용어 단어는 추후 구해서 정리한다.
        """

    def _get_high_frequency_words(self):
        article_words = Counter()
        for article in self.article_list:
            article_words.update(article)

        common_words_set = article_words.most_common(10000)
        self.high_frequency_words_set = tuple(word for word, count in common_words_set)

    def _filter_low_frequency_word(self):
        article_num = 0
        compare_words_set = Counter(self.high_frequency_words_set)
        for article in self.article_list:
            count_result_list = []
            article_counter = Counter(article)
            count_result = article_counter & compare_words_set
            for word, value in count_result.items():
                count_result_list.append(word)

            self.article_list[article_num] = count_result_list
            article_num += 1

    def _make_word_dictionary(self):
        news_dictionary = corpora.Dictionary(self.article_list)
        news_dictionary.save('news_dictionary.dict')
        self.news_dictionary = news_dictionary

    def _make_doc_matrix(self):
        doc_matrix = []
        for doc in self.article_list:
            doc2bow_result = self.news_dictionary.doc2bow(doc)
            doc_matrix.append(doc2bow_result)

        self.doc_matrix = doc_matrix
        corpora.MmCorpus.serialize('news_corpus.mm', doc_matrix)

    def _make_gensim_model(self):
        news_LDA = models.ldamodel.LdaModel
        news_model = news_LDA(self.doc_matrix,
                              num_topics = self.topic_num,
                              id2word = self.news_dictionary,
                              passes = 100)
        news_model.save('news_train_file.model')

        self.news_model = news_model

    def _draw_news_model(self):
        prepared_data = gensimvis.prepare(self.news_model,
                                          self.doc_matrix,
                                          self.news_dictionary)

        save_html(prepared_data, "news_data.html")


if __name__ == '__main__':
    news_file = '20181228_output_text.txt'
    data = NewsMining(news_file)
    data._extract_noun()
    data._clean_text()
    data._get_high_frequency_words()
    data._filter_low_frequency_word()
    data._make_word_dictionary()
    data._make_doc_matrix()
    data._make_gensim_model()
    data._draw_news_model()
