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
        1. n개 신문사의 주소를 얻는다.(limit=10, 10개)
        2. 입력된 날짜를 주소에 추가하고 타입을 신문으로 설정한다.
        3. 10개의 주소에서 각 신문사별 n면 주소를 다시 얻는다.
        4. 각각의 n면 주소에서 가지고 있는 기사들 주소를 얻는다.
        5. 기사들 주소에서 텍스트를 parsing 한다.
        """

        news_office = 'https://news.naver.com/main/officeList.nhn'
        naver_news = 'https://news.naver.com/'
        news_type = '&listType=paper'

        press_list = []
        press_soup = get_html(news_office)
        press_front_info = press_soup.find_all('div', id="groupOfficeList")[0]
        press_front_url = press_front_info.find_all('a', limit=10)

        for parsing in press_front_url:
            parsing_get = parsing.get('href')
            press_url = f'{naver_news}{parsing_get}{news_type}'
            press_list.append(press_url)

        today_press = self._add_today_date(press_list)
        page_list = self._arrange_news_page_url(today_press)
        news_url = self._get_news_url(page_list)

        return news_url

    def _add_today_date(self, press_list):
        week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        find_date = date(self.year, self.month, self.day).strftime("%Y%m%d")
        find_day = date(self.year, self.month, self.day).weekday()
        if 'sun' == week[find_day]:
            raise ValueError('sunday 뉴스는 구할 수 없습니다. 다른 날을 입력해 주세요.')
        else:
            search_date = f'&date{find_date}'
        for num in range(len(press_list)):
            press_list[num] = press_list[num] + search_date

        return press_list

    def _arrange_news_page_url(self, today_main_list):
        news_paper_page_list = []
        for journal_today_url in today_main_list:
            ret = self._get_page_number(journal_today_url)
            news_paper_page_list.append(ret)

        return news_paper_page_list

    def _get_page_number(self, today_url):
        journal_main_dict = {}
        journal_page = get_html(today_url)
        parsing_page = journal_page.find_all('div', class_='topbox_type6')[0]
        internal_page = parsing_page.find_all('a')

        page_number_list = []
        for parsing in internal_page:
            parsing_result = parsing.get('href')
            page_number = f'{"&"}{parsing_result.split("&")[-1]}'
            page_number_list.append(page_number)

        journal_main_dict[today_url] = page_number_list

        parsing_page_list = []
        for url, page_list in journal_main_dict.items():
            for page_num in page_list:
                ret = url + page_num
                parsing_page_list.append(ret)

        return parsing_page_list

    def _get_news_url(self, press_section_list):

        def get_uploaded_url(source):
            news_url_collection = []
            news_source_data = source.find_all('ul', class_="type13 firstlist")
            for url_data in news_source_data:
                url_source = url_data.select('a')
                for parsing in url_source:
                    news_url_parsing_result = parsing.get('href')
                    if news_url_parsing_result not in news_url_collection:
                        news_url_collection.append(news_url_parsing_result)

            return news_url_collection

        parsing_url = []

        for press_sections in press_section_list:
            for news_url in press_sections:
                news_source = get_html(news_url)
                news_url_source = get_uploaded_url(news_source)
                parsing_url += news_url_source

                break

        parsing_url = list(OrderedDict.fromkeys(parsing_url))

        return parsing_url

    def get_result(self):

        data_set = self._get_news_data_set(parsing_url)

        self._save_file(self.OUTPUT_URL, parsing_url)
        self._save_file(self.OUTPUT_TEXT, data_set)

        print('result good')

    def _get_news_data_set(self, parsing_url):
        news_data = []
        for news in parsing_url:
            ret = self._parse_article(news)
            news_data.append(ret)

        return news_data

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




if __name__ == '__main__':
    news_ = DailyNewsCrawling()
    news_.get_ten_journal_url()
    news_.get_result()