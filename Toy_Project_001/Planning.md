Toy_Project_001
===================================

Daily News crawler & Topic Modeling
-----------------------------------

## Project 참가자(who)

* 참가자 : wonny
-----------------------------------

## Project 배경(why)

* 10대 일간지 뉴스를 다 보고 싶은 마음이 있다.
* 물리적으로 시간을 낼 수 없다. 그래서 키워드 추출 프로그래밍 작업을 통해 간접적으로 뉴스 파악
-----------------------------------

## Project 목적(what)

* Python을 이용하여 10대 일간지 뉴스 crawler 제작
* Crawlering 한 뉴스를 활용하여 키워드 추출 코드 작성
* 기능적 완결성에 중점을 둔다.

### Project 목표 1

* Python을 이용한 web crawler 제작, 사용 도구 학습
  - Chrome 개발자 모드 사용하여 HTML 구조 학습
  - Python library requests 활용법 학습
  - Python library BeautifulSoup 활용법 학습

### Project 목표 2

* crawlering한 뉴스 기사 정제 연습
  - 불용어 처리 방법 리서치
  - 정규식 표현 코드 리서치
  - Python replace를 효과적으로 사용하기

### Project 목표 3

* Topic modeling을 이용하여 뉴스 기사 키워드 추출
  - Python library gensim 복습
  - Topic modeling 복습
-----------------------------------

## Project 진행 방법(how)

* Python web crawler 제작하여 10대 일간지 뉴스 기사를 텍스트 파일로 만든다.
  1. 각 언론사 접속 url parsing
  2. 각 언론사 별 신문 1면~n면 url paring
  3. 각 언론사 신문 n면에 포함된 기사 주소 parsing
  4. 각 기사 주소를 텍스트 파일에 저장
  5. 주소가 저장된 텍스트 파일을 호출하여 기사(한글 텍스트)를 parsing 후 텍스트 파일로 저장
    - 저장과 동시에 치환, 불용 단어 처리 진행

* 기사에서 명사를 추출한 후 gensim을 이용하여 Topic modeling을 구현한다.
  1. konlpy를 이용하여 뉴스 기사 텍스트 파일로부터 명사 추출
  2. gensim을 이용하여 Topic modeling 작업 진행
  3. PyLDAvis를 이용하여 Topic modeling 결과 시각화

### crawlering 작업에 사용 할 library
* beautifulsoup : https://www.crummy.com/software/BeautifulSoup/bs4/doc/
* requests : http://docs.python-requests.org/en/master/user/quickstart/

### Topic modeling 작업에 사용 할 library
* konlpy : https://konlpy-ko.readthedocs.io/ko/v0.4.3/
* gensim : https://radimrehurek.com/gensim/
* pyLDAvis : https://github.com/bmabey/pyLDAvis
-----------------------------------

## Project 예상 소요 시간(1일 = 8시간 기준)
* python crawler제작을 위한 관련 사항 학습 : 1일
* crawler를 이용한 10대 뉴스 저장 : 1일
* text nlp 처리 : 1일
* topic modeling 처리 후 시각화 : 1일
* 작업 재시작 예정 날짜 : 2019/05/01~
-----------------------------------

## Project 작업 환경(where)
* python 3.7.0
-----------------------------------

## Project 예상 결과(result)
* 10대 일간지 신문을 텍스트 파일로 저장
* 당일의 주요 이슈를 시각화로 나타냄
