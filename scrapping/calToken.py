import json
import decimal
import math
import time

import requests
import pandas as pd
import pymysql as my
import pika
from pika import credentials

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def selectAccount():
    row = None  # 쿼리 결과
    connection = None
    try:

        connection = my.connect(host='10.100.1.191',  # 루프백주소, 자기자신주소
                                user='root',  # DB ID
                                password='root',  # 사용자가 지정한 비밀번호
                                database='ra_data',
                                port=13306,
                                cursorclass=my.cursors.DictCursor  # 딕셔너리로 받기위한 커서
                                )
        cursor = connection.cursor()

        sql = '''
        select dea.ticker_symbol, `position`, close_price from rebalance_target_weight rtw,(select
	*
from(
	select
		*
	from daily_etf_adj dea 
	where (ticker_symbol, `date`) in (
		select ticker_symbol, max(`date`) as date_time
		from daily_etf_adj group by ticker_symbol
	)
	order by `date` desc
) t
group by t.ticker_symbol) dea
where dea.ticker_symbol = rtw.ticker_symbol ;
        '''
        cursor.execute(sql)  # 커리 실행
        row = cursor.fetchall()

        # print( row )
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
        print('종료')
    # 결과를 리턴한다.
    return row
def web_request(method_name, url, dict_data, is_urlencoded=True):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
    method_name = method_name.upper()  # 메소드이름을 대문자로 바꾼다
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')

    if method_name == 'GET':  # GET방식인 경우
        response = requests.get(url=url, params=dict_data)
    elif method_name == 'POST':  # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})

    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else:  # 문자열 형태인 경우
        return {**dict_meta, **{'text': response.text}}

def callback(ch, method, properties, body):

    body = str(body)
    body = int(body.replace('b', '').replace("'", ''))
    row = selectAccount()
    df = pd.DataFrame(row)
    account = body

    for i in range(0, len(row)):
        buyPrice = account * df.iloc[i]['position']
        token = buyPrice / df.iloc[i]['close_price']
        token = math.trunc(token)
        print(df.iloc[i]['ticker_symbol'] + " 구매 개수 : " + str(token) + "개")
        url = 'http://10.100.0.61:9090/api/v1/trading'
        data = {"amount": int(token),
                "orderPosition": "buy",
                "portfolioName": "portfolio(T)",
                "price": int(df.iloc[i]['close_price']),
                "tickerSymbol": str(df.iloc[i]['ticker_symbol']),
                "tradingName": "AIRI-RA",
                "userId": "31"
                }

        print(data)
        response = web_request(method_name='POST', url=url, dict_data=data, is_urlencoded=False)
        print(response)
        time.sleep(1)
    return body

if __name__ == '__main__':
    # 테스트

    cred = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='10.100.1.126', credentials=cred))
    channel = connection.channel()


    print('Waiting for logs')

    channel.basic_consume(
        queue='account', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
