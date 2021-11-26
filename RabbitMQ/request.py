import json
import pika
import sys

cred = pika.PlainCredentials('user', 'pwd')
connection = pika.BlockingConnection(
  pika.ConnectionParameters(host='host_ip'),credentials=cred)
channel = connection.channel()

channel.exchange_declare(exchange='queue_name')#, exchange_type='fanout')

param = {
  'company': 'ebest',
  'command': 'request',
  'trcode': 't0424',
  'data': {
	  'accno': '', #계좌번호
	  'passwd': '', #계좌비밀번호
	  'prcgb': '1', #단가구분 1:평균단가, 2:BEP단가
	  'chegb': '2', #체결구분 0:결제기준잔고, 2:체결기준(잔고 0 아닌 종목만 조회)
	  'dangb': '0', #단일가구분 0:정규장, 1:시간외단일가
	  'charge': '0', #제비용포함여부 0:제비용미포함, 1:제비용포함
  }
}
message = json.dumps(param)
channel.basic_publish(exchange='queue_name', routing_key='', body=message)
print(' [x] Sent %r' % message)
connection.close()
