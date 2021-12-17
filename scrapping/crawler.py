import datetime
import requests
import time
import re
import json
from bs4 import BeautifulSoup

start = time.time()
file = open('시사게시판.json', 'w', encoding='utf-8')
total_list = ""

file.write("{ \"paxnet\": [")
for page in range(1, 501):
    # N00801 - 거래소 시황, N10983- 코스닥 시황, N00820 - 강추이종목
    # N10716 - 전업투자자, N10841 - 자유게시판, N00802 - 시사게시판
    page_cate = "N00802"
    req = requests.get('http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=' + page_cate + '&page=' + str(page))
    html = BeautifulSoup(req.text, 'html.parser')

    request_header = {'referer' : 'http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=N00820&page='+str(page),
                      'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    json_url = 'http://www.paxnet.co.kr/tbbs/bbsWrtRecentInfo.json'
    req = requests.get(json_url, headers=request_header)

    tr_list = html.select('#comm-list')

    for tr in tr_list:

        for i in range(1, 31):

            total = tr.find_all('li')[i] #전체 리스트

            cate = total.find('span', {'class': 'el-ellipsis'}) #카테고리

            title = total.find('a', {'class': 'best-title'})  #제목

            href = total.find('p').get('id')  #내용을 가지고오기 위한 주소 탐색
            href = href.replace('tit_', '')

            write_date = total.find('span', 'data-date-format')  #작성일
            write_date = str(write_date.get_attribute_list("data-date-format"))[2:30].replace('KST ', '')
            write_date = str(datetime.datetime.strptime(write_date, '%a %b %d %H:%M:%S %Y'))

            write_timestamp = time.mktime(datetime.datetime.strptime(write_date, '%Y-%m-%d %H:%M:%S').timetuple()) #작성일 timestamp
            write_timestamp = str(write_timestamp)

            writer = total.find('span', {'class': 'nick-badge-small'}) #작성자
            writer = str(writer)
            writer = re.sub('<.+?>', '', writer, 0).strip()

            req2 = requests.get('http://www.paxnet.co.kr/tbbs/view?id=' + page_cate + '&seq=' + str(href)) #본문 내용을 얻기위한 주소
            html2 = BeautifulSoup(req2.text, 'html.parser')
            content = html2.select_one("#bbsWrtCntn > p")

            if content is None:
                content = ""
            else:
                content = content.text.replace('"', "'")

            view = html2.select_one(".viewer")
            if view is None:
                view = ""
            else:
                view = view.text.replace("조회", '')

            thumb = html2.select_one('#recommendCount')
            if thumb is None:
                thumb = ""
            else:
                thumb = thumb.text

            if cate is None:
                cate = ""
                total_list = {'title': title.text.replace('"', "'"), 'content': content, 'write_date': write_date,
                              'write_timestamp': write_timestamp,
                              'view': view, 'writer': writer, 'thumb': thumb, 'cate': cate}
            else:
                total_list = {'title': title.text.replace('"', ""), 'content': content, 'write_date': write_date, 'write_timestamp': write_timestamp,
                              'view': view, 'writer': writer, 'thumb': thumb, 'cate': cate.text}

            file.write(json.dumps(total_list, ensure_ascii=False))
            file.write(", \n")
    print("\n 진행 상황 : " + str(page) + "/500 " +"\n=====================")
file.write("]}")
file.close()

sec = time.time() - start
times = str(datetime.timedelta(seconds=sec)).split(".")
times = times[0]
print("작업 완료까지 걸린 시간 : " + times)