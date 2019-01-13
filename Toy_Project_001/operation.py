from news_parser import DailyNewsCrawling
from news_modeling import NewsModeling


def save_news_text():
    news = DailyNewsCrawling(2019, 1, 12)
    news.get_news_url()
    news.get_news_text()


def save_news_modeling():
    data = NewsMining()
    train_data_set = data.arrange_articles('output_text.txt')
    data.make_model(train_data_set)
    data.draw_news_model()


def main():
    save_news_text()
    save_news_modeling()


if __name__ == '__main__':
    main()
