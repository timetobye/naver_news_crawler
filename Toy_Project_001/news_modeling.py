import gensim
import warnings
import os
from konlpy.tag import Mecab
from collections import Counter
from gensim import corpora
from gensim import models
from gensim.models import LdaModel
from pyLDAvis import gensim as gensimvis
from pyLDAvis import display
from pyLDAvis import save_html
warnings.filterwarnings(action='ignore')


class NewsModeling:

    def __init__(self, topic_num=40):
        self.topic_num = topic_num

    def arrange_articles(self, file_name):

        articles = self._extract_noun(file_name)
        cleaned_articles = self._clean_text(articles)
        high_frequency_words = self._get_high_frequency_words(cleaned_articles)
        data_set = self._filter_low_frequency_word(cleaned_articles,
                                                   high_frequency_words)

        return data_set

    def make_model(self, data_set):
        self._make_word_dictionary(data_set)
        self._make_doc_matrix(data_set)
        news_model = self._make_gensim_model()

        return news_model

    def draw_news_model(self):
        current_path = os.getcwd()
        file_path = f'{current_path}{"/news_train_model.model"}'
        model = LdaModel.load(file_path)
        prepared_data = gensimvis.prepare(model,
                                          self.doc_matrix,
                                          self.news_dictionary)

        save_html(prepared_data, "news_data.html")

    def _extract_noun(self, txt_file):
        mecab = Mecab()
        article_list = []
        with open(txt_file, 'r') as file:
            for article in file:
                extracted_noun = mecab.nouns(article)
                article_list.append(extracted_noun)

        return article_list

    def _clean_text(self, article):
        article_num = 0
        for split_article in article:
            article[article_num] = list(filter(lambda x: len(x) >= 2, split_article))
            article_num += 1

        return article

    # def _adapt_stopwords(self):
    #     """
    #     불용어 단어는 추후 구해서 정리한다.
    #     """

    def _get_high_frequency_words(self, clean_text):
        article_words = Counter()
        for article in clean_text:
            article_words.update(article)

        common_words_set = article_words.most_common(10000)
        high_frequency_words_set = tuple(word for word, count in common_words_set)

        return high_frequency_words_set

    def _filter_low_frequency_word(self, article_list, high_frequency_words):
        article_num = 0
        compare_words_set = Counter(high_frequency_words)
        for article in article_list:
            count_result_list = []
            article_counter = Counter(article)
            count_result = article_counter & compare_words_set
            for word, value in count_result.items():
                count_result_list.append(word)

            article_list[article_num] = count_result_list
            article_num += 1

        return article_list

    def _make_word_dictionary(self, train_data):
        self.news_dictionary = corpora.Dictionary(train_data)
        self.news_dictionary.save('news_dictionary.dict')

    def _make_doc_matrix(self, train_data):
        self.doc_matrix = []
        for doc in train_data:
            doc2bow_result = self.news_dictionary.doc2bow(doc)
            self.doc_matrix.append(doc2bow_result)

        corpora.MmCorpus.serialize('news_corpus.mm', self.doc_matrix)

    def _make_gensim_model(self):
        news_lda = models.ldamodel.LdaModel
        model = news_lda(self.doc_matrix,
                         num_topics=self.topic_num,
                         id2word=self.news_dictionary,
                         passes=100)
        model.save('news_train_model.model')

        return model
