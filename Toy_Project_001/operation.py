import argparse
from news_parser import DailyNewsCrawling
from news_modeling import NewsModeling


def get_news(year, month, day):
    # scrapping news text file from 10 press company in Naver news.
    news = DailyNewsCrawling(year, month, day)
    news_url_list = news.get_news_url()
    news_text_list = news.get_news_text(news_url_list)

    return news_text_list
    

def make_lda_model_with_news(news_text):
    # make a lda model from news and draw a topic modeling graph.
    data = NewsModeling()
    train_data_set = data.arrange_articles(news_text)
    data.make_model(train_data_set)
    data.draw_news_model()


def main():
    year, month, day = args.year, args.month, args.day
    news_text_list = get_news(year, month, day)
    make_lda_model_with_news(news_text_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--year',
        type=int,
        help='input year data, ex) 2018, 2019'
    )
    parser.add_argument(
        '--month',
        type=int,
        help='input month data, ex) 1, 10, 12'
    )
    parser.add_argument(
        '--day',
        type=int,
        help='input year data, ex) 1, 12, 31'
    )
    args = parser.parse_args()
    main()
