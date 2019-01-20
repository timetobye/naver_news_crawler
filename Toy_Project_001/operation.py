from news_parser import DailyNewsCrawling
from news_modeling import NewsModeling


def save_news_text():
    # scrapping news text file from 10 press company in Naver news.
    news = DailyNewsCrawling(2019, 1, 12)
    today_news_url_list = news.get_news_url()
    today_news_text_list = news.get_news_text(today_news_url_list)
    

def save_news_modeling():
    # create a model from news_text and draw a graph using gensim model.
    data = NewsModeling()
    train_data_set = data.arrange_articles('output_text.txt')
    data.make_model(train_data_set)
    data.draw_news_model()


def main():
    save_news_text()
    save_news_modeling()


if __name__ == '__main__':
    main()
