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

def selectClosePrice():
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
select rr.ticker_symbol, `position` , rebalance_id, close_price from rebalance_result rr , (select
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
)t group by t.ticker_symbol) dea
where rr.rebalance_id = (select max(r.rebalance_id) from rebalance r where r.account_number = '55500312301')
and dea.ticker_symbol = rr.ticker_symbol 
and rr.ticker_symbol not in (select rr.ticker_symbol from rebalance_result rr ,trading_account ta  
	where rr.ticker_symbol = ta.ticker_symbol
	and rr.rebalance_id = (select max(r.rebalance_id) from rebalance r where r.account_number = '55500312301')
	and DATE_FORMAT(ta.created_at, '%Y-%m%-%d') = DATE_FORMAT(now(), '%Y-%m-%d'));
        '''
        cursor.execute(sql)  # 커리 실행
        row = cursor.fetchall()
        print(row)
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
        print('구매 개수 반환을 위한 종가 조회 종료')
    # 결과를 리턴한다.
    return row
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
select * from balance b ORDER by created_at desc limit 1;
        '''
        cursor.execute(sql)  # 커리 실행
        row = cursor.fetchall()
        # print( row )
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
        print('계좌 잔고 조회 종료')
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
def rebalance_sell():
    rebalanceSell = None  # 쿼리 결과
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
select ta.ticker_symbol, sale_available_amount ,close_price from trading_account ta, (select
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
)t group by t.ticker_symbol) dea 
where DATE_FORMAT(ta.created_at, '%Y-%m%-%d') = DATE_FORMAT(now(), '%Y-%m-%d')
and dea.ticker_symbol = ta.ticker_symbol 
and ta.ticker_symbol not in (select ticker_symbol from rebalance_result 
where rebalance_id = (select max(r.rebalance_id) from rebalance r where r.account_number = '55500312301'))
and sale_available_amount <> 0;
        '''
        cursor.execute(sql)  # 커리 실행
        rebalanceSell = cursor.fetchall()
        print(rebalanceSell)
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
        print('리벨런싱 매매 종료')
    # 결과를 리턴한다.
    return rebalanceSell

def rebalance_buy_or_sell():
    buyOrSell = None  # 쿼리 결과
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
SELECT ticker_symbol,
       sale_available_amount, 
       (`position` * balance) as buy_price, 
       FLOOR(((`position` * balance)/close_price)) as require_amount,
       close_price from (
              select ta.ticker_symbol,
                     sale_available_amount, 
                    `position`, 
                    (select balance from balance b order by created_at desc limit 1) as balance,
                     close_price 
FROM trading_account ta INNER JOIN rebalance_result rr 
ON ta.ticker_symbol = rr.ticker_symbol, 
(select * from 
         (select * from daily_etf_adj dea 
          where (ticker_symbol, `date`) in (select ticker_symbol, max(`date`) as date_time 
           from daily_etf_adj group by ticker_symbol) 
           order by `date` desc)t 
           group by t.ticker_symbol) dea  
WHERE DATE_FORMAT(ta.created_at, '%Y-%m%-%d') = DATE_FORMAT(now(), '%Y-%m-%d')
and rr.rebalance_id = (select max(r.rebalance_id) from rebalance r where r.account_number = '55500312301')
and dea.ticker_symbol = ta.ticker_symbol) ta;
        '''
        cursor.execute(sql)  # 커리 실행
        buyOrSell = cursor.fetchall()
        print(buyOrSell)
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
        print('리벨런싱 매매 종료')
    # 결과를 리턴한다.
    return buyOrSell

def callback(ch, method, properties, body):
    body = str(body)
    body = body.lstrip('b').replace("'", '')
    row = selectClosePrice()
    df = pd.DataFrame(row)
    print(body)

    #리벨런스 일괄 매도 필요 종목 조회
    rebalanceSell = rebalance_sell()
    rebalanceSellDataFrame = pd.DataFrame(rebalanceSell)

    #리벨런스 추가 매수, 매도 필요 종목 조회
    buyOrSell = rebalance_buy_or_sell()
    buyOrSellDataFrame = pd.DataFrame(buyOrSell)

    accountDataFrame = pd.DataFrame(selectAccount())
    account = int(accountDataFrame.iloc[0]['balance'])

    if body == "trading_buy":
        for i in range(0, len(row)):
            buyPrice = account * df.iloc[i]['position']
            token = buyPrice / df.iloc[i]['close_price']
            token = math.trunc(token)
            print(df.iloc[i]['ticker_symbol'] + " 구매 개수 : " + str(token) + "개")
            url = 'http://10.100.0.61:9090/api/v1/trading'
            data = {"amount": int(token),
                    "orderPosition": "buy",
                    "portfolioName": "Portfolio(T)",
                    "price": int(df.iloc[i]['close_price']),
                    "tickerSymbol": str(df.iloc[i]['ticker_symbol']),
                    "tradingName": "AIRI Dynamic Alpha",
                    "accountNumber": "55500312301"
                    }
            print(data)
            # response = web_request(method_name='POST', url=url, dict_data=data, is_urlencoded=False)
            # print(response)
            time.sleep(1)
    elif body == "rebalance":
        for i in range(0, len(rebalanceSell)):
            url = 'http://10.100.0.61:9090/api/v1/trading'
            data = {"amount": int(rebalanceSellDataFrame.iloc[i]['sale_available_amount']),
                    "orderPosition": "sell",
                    "portfolioName": "Portfolio(T)",
                    "price": int(rebalanceSellDataFrame.iloc[i]['close_price']),
                    "tickerSymbol": str(rebalanceSellDataFrame.iloc[i]['ticker_symbol']),
                    "tradingName": "AIRI Dynamic Alpha",
                    "accountNumber": "55500312301"
                    }
            print(data)
            # response = web_request(method_name='POST', url=url, dict_data=data, is_urlencoded=False)
            # print(response)
            time.sleep(1)

        for i in range(0, len(buyOrSellDataFrame)):
            position = ""
            amount = int(buyOrSellDataFrame.iloc[i]['require_amount']) - int(buyOrSellDataFrame.iloc[i]['sale_available_amount'])
            if amount > 0:
                position = "buy"
            else:
                position = "sell"
                amount = abs(amount)

            url = 'http://10.100.0.61:9090/api/v1/trading'
            data = {"amount": amount,
                    "orderPosition": position,
                    "portfolioName": "Portfolio(T)",
                    "price": int(buyOrSellDataFrame.iloc[i]['close_price']),
                    "tickerSymbol": str(buyOrSellDataFrame.iloc[i]['ticker_symbol']),
                    "tradingName": "AIRI Dynamic Alpha",
                    "accountNumber": "55500312301"
                    }
            print(data)
            # response = web_request(method_name='POST', url=url, dict_data=data, is_urlencoded=False)
            # print(response)
            time.sleep(1)
    else:
        print("올바르지 않은 주문 유형입니다.")
    return body
if __name__ == '__main__':
    # 테스트
    cred = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='10.100.1.126', credentials=cred))
    channel = connection.channel()
    print('Waiting for logs')
    channel.basic_consume(
        queue='rebalance', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()