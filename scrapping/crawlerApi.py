import datetime
import requests
import time
import re
import json
from flask import jsonify
from flask_restx import Resource, Namespace
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('host_ip', 'port')
db = client['dbName']
collection_currency = db['collectionName']
crawlerApi = Namespace('community', description='paxnet crawling API')

@crawlerApi.route('/<string:page_cate>/<int:page_end>')
class PaxnetRecommend1(Resource):

  def get(self, page_cate, page_end):
    ''' N00801(거래소 시황) / N10983(코스닥 시황) / N00820(강추이종목) / N10716(전업투자자) / N10841(자유게시판) / N00802(시사게시판) '''
    return jsonify(main(page_cate, page_end))

def main(page_cate, page_end):
    now = datetime.datetime.now()
    oneMinuteLater = (now - datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')

    result = []

    for page in range(1, page_end + 1):
        # N10716 - 전업투자자, N10841 - 자유게시판, N00802 - 시사게시판
        # N00801 - 거래소 시황, N10983- 코스닥 시황, N00820 - 강추이종목

        req = requests.get('http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=' + page_cate + '&page=' + str(page_end))
        html = BeautifulSoup(req.text, 'html.parser')

        tr_list = html.select('#comm-list')

        for tr in tr_list:

            for i in range(1, 31):

                total = tr.find_all('li')[i] #전체 리스트

                cate = total.find('span', {'class': 'el-ellipsis'}) #카테고리

                title = total.find('a', {'class': 'best-title'})  #제목
                title = title.text.replace('"', "'")

                href = total.find('p').get('id')  #내용을 가지고오기 위한 주소 탐색
                href = href.replace('tit_', '')

                write_date = total.find('span', 'data-date-format')  #작성일
                write_date = str(write_date.get_attribute_list("data-date-format"))[2:30].replace('KST ', '')
                write_date = str(datetime.datetime.strptime(write_date, '%a %b %d %H:%M:%S %Y'))

                compareDate = write_date[:16]

                write_timestamp = time.mktime(datetime.datetime.strptime(write_date, '%Y-%m-%d %H:%M:%S').timetuple()) #작성일 timestamp
                write_timestamp = str(write_timestamp)

                writer = total.find('span', {'class': 'nick-badge-small'}) #작성자
                writer = str(writer)
                writer = re.sub('<.+?>', '', writer, 0).strip()

                req2 = requests.get('http://www.paxnet.co.kr/tbbs/view?id=' + page_cate + '&seq=' + str(href)) #본문 내용을 얻기위한 주소
                html2 = BeautifulSoup(req2.text, 'html.parser')
                content = html2.select_one("#bbsWrtCntn > p")
                if oneMinuteLater == compareDate:
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
                    else:
                        cate = cate.text

                    result.append({
                        'title': title,
                        'content': content,
                        'write_date': write_date,
                        'write_timestamp': write_timestamp,
                        'view': view,
                        'writer': writer,
                        'thumb': thumb,
                        'cate': cate
                    })
    collection_currency.insert_many(result)
    json_result = json.loads(json.dumps(result, default=str, ensure_ascii=False))
    if json_result is None:
        return '[]'
    return json_result