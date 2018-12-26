Toy_Project_001
===================================

Daily News crawler & Topic Modeling
-----------------------------------

## Toy_Project 목적

### News
* 8대 일간지 crawler 후 Topice modeling을 이용해 당일의 가장 이슈가 무엇인지 알아본다.
* 이슈 중심으로 기사 서치 시간을 줄인다.

### Programming
* 해보고 싶은 것(web crawler), 할 수 있는 것(string 처리), 해봤던 것(topic modeling)
  - 도전과 할 수 있는 것을 섞어서 현재 할 수 있는 최대 결과가 어디인지 가늠해본다.
* 가독성 높은 코드 작성
  - clean code 책에서 강조한 내용과 pep8을 최대한 지켜서 작성해본다.
  - 처음부터 끝까지 코드를 작성하고 다른 사람들이 이해 할 수 있는 수준으로 작성한다.
  - 코드 리뷰를 부탁해 본다.(코드 리뷰는 부끄러운 게 아니다) ~~물론 받을 때도 그런 생각을 가져야 한다..~~
  
## Toy_Project 배경

* 프로젝트 기간에 힘들었던 것 중 하나는 뉴스를 꼼꼼히 볼 수 없다는 점이 있었다.
  - ~~세상이 어떻게 돌아가는지 알아야 사는 맛도 있지...~~
  - 신변잡기 뉴스는 원래도 안 봤지만, 뉴스를 안 보니 그런거라도 봐야하나 생각이 들었다. 뉴스에 대한 갈증
  
* News crawler는 상필님께서 만들어 주신 것을 사용해 본적이 있다.
  - 그러나 node.js으로 구현되어 현재의 내가 이해할 수 없는 영역이었다.
  - python으로 가능함을 알기에 가을부터 도전해보고 싶은 분야였다.
  
* 업무 과정 중 파편적으로 진행헀던 부분을 Toy Project를 하면서 정리해보고 싶었다.

* 한국어 자연어 처리 대표 library인 konlpy가 진화를 하는 중
  - koshort : https://github.com/koshort/koshort
  - konlpy를 할 때는 최신 단어 처리가 어려웠는데 koshort를 이용해서 향상된 자연어 처리를 해보고 싶다.

## Toy_Project 일정

### 예상 소요 시간(1일 = 8시간 기준)
* python crawler 학습 : 2일(max)
  - crawler를 이용한 8대 뉴스 저장 : 1일(max)
* text nlp 처리 : 2일(max)
* topic modeling 처리 : 1일(max)
* ~~이거대로 될리가 없지~~

## Toy_Project 개념

### programing 영역

* crawler
* nlp
* topic modeling

### 준비사항

* https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=081
  - 네이버 10대 뉴스 종합 페이지
  - 상필님이 만드신 node.js은 서울신문 페이지만 긁어왔던 것으로 기억한다.
    + 물론 주소를 변경해주면 다른 신문도 가능하긴 했었다. 그것을 응용해보려고 한다.

* 자연어 처리 방법에 대한 이해, 웹서치
* topic modeling을 위한 gensim library

### 사용 library(추가 예정)

* gensim : https://radimrehurek.com/gensim/
* beautifulsoup : https://www.crummy.com/software/BeautifulSoup/bs4/doc/
* requests : http://docs.python-requests.org/en/master/user/quickstart/
* urllib : https://docs.python.org/3/library/urllib.html
* pyLDAvis : https://github.com/bmabey/pyLDAvis

## Toy_Project 예상 어려움

1. crawler 만들기 위한 배경 지식 쌓기
2. News 페이지만 crawlering 할 수 있는 방법
3. crawlering 결과를 정제하는 과정에 대한 정규식 적용 외

## Toy_Project 예상 결과

### News
* 당일 뉴스의 핵심 단어들을 pyLDAvis로 시각화한다.

### programming
* crawler, nlp 경험치 증가
* clean code, pep8 적용 여부 확인
