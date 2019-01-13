from news_parser import DailyNewsCrawling


def main():
    news = DailyNewsCrawling(2019, 1, 12)
    news.get_news_url()
    news.get_news_text()


if __name__ == '__main__':
    main()
