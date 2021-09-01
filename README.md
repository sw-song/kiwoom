# kiwoom
kiwoom api를 활용한 실시간 종목정보 조회 & 자동매매 

## 폴더 구조
```
.
# 동작코드
|--main.py
|--kiwoom.py
|  |--config
|     |--slack.py
_____________________________________________________
# 전체구성(테스트/연습용 코드 포함)
|--main.py
|--kiwoom.py
|--test_main.py
|  |--kiwoom
|     |--api.py
|  |--practice
|     |--1~6 : PyQt 활용 - 로그인, 이벤트 처리, TR 요청
|     |--7~8 : python에서 sqlite 기본 사용법
|     |--9~11: api 연결 db구축
|     |--12  : class연습
|     |--99  : pykiwoom 활용 - 로그인 및 일봉데이터 수집
|  |--data
|  |--config
|     |--errCode.py
|     |--kiwoomType.py
|     |--slack.py
|  |--files
|     |--condition_stock.txt
|
|--.gitignore
|--README.md
```
---

## 주요 모듈&함수
1. QAxWidget.setControl()
- 파이썬이 .ocx 확장자를 컨트롤 할 수 있도록 함


## 에러 기록
**window 관련 에러**
1. MAC에서 생성한 REPO를 WINDOW에서 다룰 경우(LF/CRLF 에러)
> 해결 방법 : 
```zsh
git config --global core.autocrlf true
```

**kiwoom api 관련 에러**
1. 로그인과 동시에 발생하는 키움 api 이벤트 - 아래 코드 중복 실행시 에러 발생.
```python
self.kiwoom.OnEventConnect.connect(self.login_state)
```
> 해결 X

**pyqt 관련 에러**
1. pyqt app 반복 생성시 에러(kernel dead)
> 해결 방법 : 최초 실행시 인스턴스로 할당해줘야 중복 실행 가능
```python
app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
```

## reference
1. [퀀트투자를 위한 키움증권 API(파이썬버전), 조대표](https://wikidocs.net/book/1173)
2. [파이썬으로 배우는 알고리즘 트레이딩, 조대표](https://wikidocs.net/book/110)
3. [파이썬으로 배우는 알고리즘 트레이딩(소스코드), 조대표](https://github.com/pystockhub/book)
4. [손가락 하나 까딱하지 않는 주식 거래 시스템 구축(위키북스), 장용준(프로그램동산)](https://wikibook.co.kr/pystock/)
5. [(Youtube)24시간 주식매매 자동화 구축하기[open API+], 프로그램동산](https://www.youtube.com/watch?v=K9x3HDSdrjo&list=PLDtzZPtOGenaSknTbsb6x6L39V0VPz_rS)
6. [[Python]키움API 조건검색 텔레그램 알림 만들기(1), 개인블로그(코딩으로 자아실현)](https://kminito.tistory.com/36)
