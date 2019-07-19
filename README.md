naver_news_crawler
---------------------
![alt text](https://img.shields.io/badge/Python-3.7-red.svg)
![alt text](https://img.shields.io/badge/LDA-Topic%20Modeling-brightgreen.svg)
![alt text](https://img.shields.io/badge/Crawler-News-yellowgreen.svg)
![alt text](https://img.shields.io/badge/results-report-blue.svg)
![alt text](https://img.shields.io/badge/data-web-orange.svg)


> 종합 일간지 10개를 크롤링 하고 Topic modeling을 이용해 오늘의 뉴스 키워드를 알아봅니다.

:newspaper: Introduction
----------------------------

신문 읽기를 무척 좋아했던 한 남자는, 일을 하기 시작하면서 좋아하던 신문을 볼 시간을 잃어버렸습니다.
사실 핑계같은 이야기일수도 있지만, 개발을 막 시작하면서 느꼈던 배움의 즐거움이 신문 읽는 것보다 더 큰 것이었기에 신문에게 잠시 안녕을 고했습니다.
그러나 힘든 프로젝트를 하면서 뉴스 조차 못 보는 상황에 이르게 됐고, 결국 내면 깊숙히 잠들어 있던 신문에 대한 욕구가 피어오르기 시작했습니다.

본 연구에서는 네이버에서 제공하는 종합 일간지 10개(경향, 국민, 동아, 문화, 서울, 세계, 조선, 중앙, 한겨레, 한국)를 웹 크롤링(web crawling) 하고,
크롤링 된 뉴스 기사에서 자연어 처리를 진행합니다. 처리 된 결과를 바탕으로 어떤 단어들이 오늘의 기사에 많이 사용되고, 분포를 가지는지 Gensim의 Topic modeling을
이용하여 분석을 수행합니다. 마지막으로 LDA 모델을 시각화 할 수 있는 pyLDAvis를 이용해서 html 파일로 저장합니다.

한국어 자연어 처리는 영어보다 어렵다고 합니다. 그럼에도 불구하고 위대한 선구자들께서 만들어 놓은 좋은 라이브러리를 이용하면 무서울 게 없습니다.
다만 mecab의 기본 사전에서 사전 추가를 하지 않았기 때문에 완벽하게 뉴스 기사를 분석 할 수는 없습니다. 
그러나 뉴스는 가장 한글 문법 규칙에 맞는 단어를 사용하기 때문에 어느 정도 수준의 분석은 진행 할 수 있습니다.
기본적으로 월요일 ~ 토요일까지의 기사들을 가져올 수 있으며, 일요일은 뉴스가 제공되지 않기 때문에 가져 올 수 없습니다.

저는 하루에 한 번 코드를 실행하고 당일 신문에 나온 내용을 살펴보곤 합니다. :newspaper_roll:
데이터 분석과 개발을 배우면서 처음 했던 Toy project였기 때문에 혼자 하는 것이 쉽지 않았지만 무척 즐거웠습니다.
~~크리스마스에 솔로라 작업을 했었던 기억~~ 바쁜 시간에도 코드를 봐주시고 조언을 해주신 bloodwind 님께 항상 감사드립니다.

:keyboard: 설치방법
-------------
mecab을 사용하고 있기 때문에 Mac 환경에서만 사용 가능합니다.

### mecab 설치
```
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

### library
```
pip install -r requirements.txt
```

### 주의 사항
- library 설치 시 오류가 발생할 경우 에러 메시지로 검색하여 대응해주시기 바랍니다.


:desktop_computer: 사용 방법
-----------------------------
