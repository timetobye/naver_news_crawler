import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import OrderedDict


def get_html(url):
    pages = requests.get(url)
    page_soup = BeautifulSoup(pages.text, 'html.parser')

    return page_soup


class DailyNewsCrawling:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def get_news_url(self):

        """
        1. 10개 신문사의 주소를 얻는다.
        2. 10개의 주소에서 각 신문사별 n면 주소를 다시 얻는다.
        3. 각각의 n면 주소에서 가지고 있는 기사들 주소를 얻는다.
        4. 기사들 주소에서 텍스트를 parsing 한다.
        """

        news_officelist = 'https://news.naver.com/main/officeList.nhn'
        naver_news = 'https://news.naver.com/'
        news_type = '&listType=paper'

        press_list = []
        press_soup = get_html(news_officelist)
        press_front_info = press_soup.find_all('div', id="groupOfficeList")[0]
        press_front_url = press_front_info.find_all('a', limit=10)

        for parsing in press_front_url:
            parsing_get = parsing.get('href')
            press_url = f'{naver_news}{parsing_get}{news_type}'
            press_list.append(press_url)


        journal_main_link_list = self._add_today_date(journal_main_link_list)
        news_paper = self._arrange_newspage_url(journal_main_link_list)
        self.news_page_result = self._arrange_parsing_url(news_paper)

    def get_result(self):

        parsing_url = self._get_news_url(self.news_page_result)
        data_set = self._get_news_data_set(parsing_url)
        # print(data_set)

        self._save_file(self.OUTPUT_URL, parsing_url)
        self._save_file(self.OUTPUT_TEXT, data_set)

        print('result good')

    def _get_news_html(self, url):
        news_mainpage_info = requests.get(url)
        news_page_soup = BeautifulSoup(news_mainpage_info.text, 'html.parser')

        return news_page_soup

    def _save_file(self, name, input_data):
        with open(name, 'a', encoding='UTF-8') as f:
            for input_value in input_data:
                f.write(input_value + '\n')

    def _parse_article(self, url):
        article_info = requests.get(url)
        article_soup = BeautifulSoup(article_info.text, 'html.parser', from_encoding='utf-8')
        article_search = article_soup.find_all('div', id="articleBodyContents")
        if len(article_search) > 0:
            text_with_html = article_search[0]
            unrefined_text = text_with_html.get_text()
            refined_text = self._replace_unused_word(unrefined_text)
        else:
            return 'None'

        return refined_text.rstrip()

    def _get_page_number(self, journal_today_url):
        journal_main_link_dict = {}
        journal_page_soup = self._get_news_html(journal_today_url)
        parsing_internal_page = journal_page_soup.find_all('div', class_='topbox_type6')
        parsing_internal_page = parsing_internal_page[0]
        internal_page = parsing_internal_page.find_all('a')

        page_number_list = []
        for parsing in internal_page:
            parsing_result = parsing.get('href')
            page_number = '&' + parsing_result.split('&')[-1]
            page_number_list.append(page_number)

        journal_main_link_dict[journal_today_url] = page_number_list

        return journal_main_link_dict

    def _add_today_date(self, journal_main_link_list):
        current_datetime = datetime.now() - timedelta(days=1) # 현재 시간 계산해서 nn시 이전이면 전날 것으로 계산하게 만들 것
        today_information = '&date=' + current_datetime.strftime("%Y%m%d")

        for num in range(len(journal_main_link_list)):
            journal_main_link_list[num] = journal_main_link_list[num] + today_information

        return journal_main_link_list

    def _replace_unused_word(self, text):

        def replace_all(sentence, dic):
            for i, j in dic.items():
                sentence = sentence.replace(i, j)
            return sentence

        replace_words_dict = dict([("\n", ""),
                                   ("ㆍ", ""),
                                   ("▶", ""),
                                   ("flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", ""),
                                   ("/", ""),
                                   ("무단전재 및 재배포 금지", "")])
        text = replace_all(text, replace_words_dict)

        cleaned_text = re.sub('[a-zA-Z]', "", text)
        cleaned_text = re.sub('[\{\}\[\]\/?;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                              '', cleaned_text)

        return cleaned_text

    def _arrange_newspage_url(self, journal_today_main_page):
        newpaper_page_list = []
        for journal_today_url in journal_today_main_page:
            ret = self._get_page_number(journal_today_url)
            newpaper_page_list.append(ret)

        return newpaper_page_list

    def _arrange_parsing_url(self, news_paper):
        parsing_page_list = []
        for daily_page in news_paper:
            for url, page_list in daily_page.items():
                for page_num in page_list:
                    ret = url + page_num
                    parsing_page_list.append(ret)

        return parsing_page_list

    def _get_uploaded_url(self, news_source):
        news_url_collection = []
        for url_data in news_source:
            source = url_data.select('a')
            for parsing in source:
                news_url_parsing_result = parsing.get('href')
                if news_url_parsing_result not in news_url_collection:
                    news_url_collection.append(news_url_parsing_result)

        return news_url_collection

    def _get_news_url(self, news_page_result):
        parsing_url = []

        for news_url in news_page_result:
            news_source = self._get_news_html(news_url)
            news_source = news_source.find_all('ul', class_="type13 firstlist")
            news_url_source = self._get_uploaded_url(news_source)
            parsing_url += news_url_source

            break

        parsing_url = list(OrderedDict.fromkeys(parsing_url))

        return parsing_url

    def _get_news_data_set(self, parsing_url):
        news_data = []
        for news in parsing_url:
            ret = self._parse_article(news)
            news_data.append(ret)

        return news_data


if __name__ == '__main__':
    news_ = DailyNewsCrawling()
    news_.get_ten_journal_url()
    news_.get_result()