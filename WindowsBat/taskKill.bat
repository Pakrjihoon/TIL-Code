@echo off
taskkill /im '프로세스.exe'


option : /t 자식프로세스 지우기
/f 강제종료

app 실행이 windows kernel에서 실행중일 경우 taskkill 이 불가능하다.
