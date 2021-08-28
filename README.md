# kiwoom
kiwoom api를 활용한 실시간 종목정보 조회 & 자동매매 

## 폴더 구조
```
.
|--main.py
|--kiwoom.py
|  |--practice
|     |--1~6 : PyQt 활용 - 로그인, 이벤트 처리, TR 요청
|     |--7~8 : python에서 sqlite 기본 사용법
|     |--9~11: class연습
|     |--99  : pykiwoom 활용 - 로그인 및 일봉데이터 수집
|  |--data
|--.gitignore
|--README.md
```
---

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
