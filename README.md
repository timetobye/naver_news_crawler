naver_news_crawler
---------------------
![alt text](https://img.shields.io/badge/Python-3.7-red.svg)
![alt text](https://img.shields.io/badge/LDA-Topic%20Modeling-brightgreen.svg)
![alt text](https://img.shields.io/badge/Crawler-News-yellowgreen.svg)
![alt text](https://img.shields.io/badge/results-report-blue.svg)
![alt text](https://img.shields.io/badge/data-web-orange.svg)


> 종합 일간지 10개를 크롤링 하여 오늘의 뉴스 키워드를 알아보

:newspaper: Introduction
----------------------------

신문 읽기를 무척 좋아했던 한 남자는, 일을 하기 시작하면서 좋아하던 신문을 볼 시간을 잃어버렸습니다.
사실 핑계같은 이야기일수도 있지만, 개발을 막 시작하면서 느꼈던 배움의 즐거움이 신문 읽는 것보다 더 큰 것이었기에 신문에게 잠시 안녕을 고했습니다.
그러나 힘든 프로젝트를 하면서 뉴스를 못 보는 상황에 이르게 됐고, 결국 내면 깊숙히 잠들어 있던 신문에 대한 욕구가 피어오르기 시작했습니다.
본 연구에서는 네이버에서 제공하는 종합 일간지 10개(경향, 국민, 동아, 문화, 서울, 세계, 조선, 중앙, 한겨레, 한국)를 웹 크롤링(web crawling) 하고,
크롤링 된 뉴스 기사에서 자연어 처리를 진행합니다. 처리 된 결과를 바탕으로 어떤 단어들이 오늘의 기사에 많이 사용되고, 분포를 가지는지 Gensim의 Topic modeling을
이용하여 분석을 수행합니다.

한국어 자연어 처리는 영어보다 쉽지 않고, 사전은 mecab의 기본 사전을 사용했기 때문에 완벽하게 뉴스 기사를 분석 할 수는 없습니다. 그러나 뉴스는
가장 한글 문법 규칙에 맞는 단어를 사용하기 때문에 어느 정도 수준의 분석은 진행 할 수 있습니다.
기본적으로 월요일 ~ 토요일까지의 기사들을 가져올 수 있으며, 일요일은 뉴스가 제공되지 않기 때문에 가져 올 수 없습니다.

저는 하루에 한 번 코드를 실행하고 당일 신문에 나온 내용을 살펴보곤 합니다. :newspaper_roll:


