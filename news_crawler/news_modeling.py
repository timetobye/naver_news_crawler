import gensim
import warnings
import os
from konlpy.tag import Mecab
from collections import Counter
from gensim import corpora
from gensim import models
from gensim.models import LdaModel
from pyLDAvis import gensim as gensimvis
from pyLDAvis import save_html as lda_visualization
warnings.filterwarnings(action='ignore')


def save_model_data(name, folder_name='lda_model'):
    folder_path = f'{os.getcwd()}{os.sep}{folder_name}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, name)

    return file_path


def load_model_data(name, folder_name='lda_model'):
    folder_path = f'{os.getcwd()}{os.sep}{folder_name}'
    file_path = os.path.join(folder_path, name)

    return file_path


class NewsModeling:

    def __init__(self, topic_num=10):
        self.topic_num = topic_num

    def make_train_news_data_list(self, news_text_list):
        articles = self._extract_noun(news_text_list)
        cleaned_articles = self._delete_single_word(articles)
        high_frequency_words = self._get_high_frequency_words(cleaned_articles)
        data_list = self._filter_low_frequency_word(cleaned_articles,
                                                    high_frequency_words)

        return data_list

    def make_lda_model(self, data_list):
        self._make_word_dictionary(data_list)
        self._make_doc_matrix(data_list)
        self._make_gensim_model()

    def make_lda_visualization(self):
        file_path = load_model_data('news_train_model.model')
        model = LdaModel.load(file_path)
        lda_prepared_data = gensimvis.prepare(model,
                                              self.doc_matrix,
                                              self.news_dictionary)
        
        lda_visualization(lda_prepared_data, "news_lda_topic_modeling.html")

    def _extract_noun(self, news_text_list):
        mecab = Mecab()
        article_list = []
        for article in news_text_list:
            extracted_noun = mecab.nouns(article)
            article_list.append(extracted_noun)

        return article_list

    def _delete_single_word(self, article_list):
        article_num = 0
        for split_article in article_list:
            article_list[article_num] = list(filter(lambda x: len(x) >= 2, split_article))
            article_num += 1

        return article_list

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
        
        news_dict_file_name = save_model_data('news_dictionary.dict')
        self.news_dictionary.save(news_dict_file_name)

    def _make_doc_matrix(self, train_data):
        self.doc_matrix = []
        for doc in train_data:
            doc2bow_result = self.news_dictionary.doc2bow(doc)
            self.doc_matrix.append(doc2bow_result)

        doc_matrix_file_name = save_model_data('news_corpus.mm')
        corpora.MmCorpus.serialize(doc_matrix_file_name, self.doc_matrix)

    def _make_gensim_model(self):
        news_lda = models.ldamodel.LdaModel
        model = news_lda(self.doc_matrix,
                         num_topics=self.topic_num,
                         id2word=self.news_dictionary,
                         passes=100)
        
        model_file_name = save_model_data('news_train_model.model')
        model.save(model_file_name)

        return model
