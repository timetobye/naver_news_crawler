import re
import requests
import warnings
import os
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from collections import OrderedDict
warnings.filterwarnings(action='ignore')


def get_html(url):
    pages = requests.get(url)
    page_soup = BeautifulSoup(pages.text, 'html.parser')

    return page_soup


def save_news_data(name, input_data, folder_name='news'):
    folder_path = f'{os.getcwd()}{"/"}{folder_name}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, name)

    with open(file_path, 'a', encoding='UTF-8') as f:
        for input_value in input_data:
            f.write(input_value + '\n')


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
        parsing_news_url_list = self._get_news_url(page_list)
        
        return parsing_news_url_list

    def get_news_text(self, parsing_url_list):
        news_text_data = []
        for parsing_url in parsing_url_list:
            ret = self._parse_article(parsing_url)
            news_text_data.append(ret)
        
        today_news_text_file_name = f'{self.find_date}{"_news_text_file"}{".txt"}'
        save_news_data(today_news_text_file_name, news_text_data)

        return news_text_data

    def _add_today_date(self, press_list):
        week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.find_date = date(self.year, self.month, self.day).strftime("%Y%m%d")
        find_day = date(self.year, self.month, self.day).weekday()
        if 'sun' == week[find_day]:
            raise ValueError('sunday 뉴스는 구할 수 없습니다. 다른 날을 입력해 주세요.')
        else:
            search_date = f'&date{self.find_date}'
        for num in range(len(press_list)):
            press_list[num] = press_list[num] + search_date

        return press_list

    def _arrange_news_page_url(self, today_press_main_page_list):
        news_paper_page_list = []
        for press_main_page in today_press_main_page_list:
            try:
                ret = self._get_page_number(press_main_page)
                news_paper_page_list.append(ret)
            except Exception as e:
                print(e)
                continue

        return news_paper_page_list

    def _get_page_number(self, today_url):
        """
        각 언론사별 뉴스 페이지(1면, 2면 ...n 면) 주소를 얻어내서 정리해주는 기능을 돕습니다.
        """
        journal_main_dict = {}
        journal_page = get_html(today_url)
        # parsing_page = journal_page.find_all('div', class_='topbox_type6')[0]
        parsing_page = journal_page.find_all('div', class_='topbox_type6')[0]
        # print(type(parsing_page))
        internal_page = parsing_page.find_all('a')
        # print('되나?')

        page_number_list = []
        for parsing in internal_page:
            parsing_result = parsing.get('href')
            page_number = f'{"&"}{parsing_result.split("&")[-1]}'
            page_number_list.append(page_number)

        journal_main_dict[today_url] = page_number_list

        press_section_list = []
        for url, page_list in journal_main_dict.items():
            for page_num in page_list:
                ret = url + page_num
                press_section_list.append(ret)

        return press_section_list

    def _get_news_url(self, press_section_list):
        parsing_url = []

        for press_sections in press_section_list:
            for news_url in press_sections:
                html_news_source = get_html(news_url)
                news_url_source = self._get_uploaded_url(html_news_source)
                parsing_url += news_url_source

                break

        parsing_url_list = list(OrderedDict.fromkeys(parsing_url))

        today_news_url_file_name = f'{self.find_date}{"_news_url_file"}{".txt"}'
        save_news_data(today_news_url_file_name, parsing_url_list)

        self.parsing_url_list = parsing_url_list

        return parsing_url_list
    
    def _get_uploaded_url(self, html_source):
        news_url_collection = []
        news_source_data = html_source.find_all('ul', class_="type13 firstlist")
        for url_data in news_source_data:
            url_source = url_data.select('a')
            for parsing in url_source:
                news_url_parsing_result = parsing.get('href')
                if news_url_parsing_result not in news_url_collection:
                    news_url_collection.append(news_url_parsing_result)

        return news_url_collection

    def _parse_article(self, url):
        article_html = requests.get(url)
        article_soup = BeautifulSoup(article_html.text, 'html.parser', from_encoding='utf-8')
        article_search = article_soup.find_all('div', id="articleBodyContents")
        if len(article_search) > 0:
            text_with_html = article_search[0]
            unrefined_text = text_with_html.get_text()
            refined_text = self._clean_text(unrefined_text)
        else:
            return 'None'

        return refined_text.rstrip()

    def _clean_text(self, text):

        def replace_unnecessary_word(sentence, dic):
            for i, j in dic.items():
                sentence = sentence.replace(i, j)
            return sentence

        replace_words_dict = dict([("\n", ""),
                                   ("ㆍ", ""),
                                   ("▶", ""),
                                   ("flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", ""),
                                   ("/", ""),
                                   ("무단전재 및 재배포 금지", "")])
        text = replace_unnecessary_word(text, replace_words_dict)

        cleaned_text = re.sub('[a-zA-Z]', "", text)
        cleaned_text = re.sub('[\{\}\[\]\/?;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                              '', cleaned_text)

        return cleaned_text
