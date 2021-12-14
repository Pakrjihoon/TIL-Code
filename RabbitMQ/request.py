import json
import pika
import sys

cred = pika.PlainCredentials('user', 'pwd')
connection = pika.BlockingConnection(
  pika.ConnectionParameters(host='host_ip', credentials=cred))
channel = connection.channel()

channel.exchange_declare(exchange='queue_name')#, exchange_type='fanout')

param = {
  'data': {
	  'key': 'value'
  }
}
message = json.dumps(param)
channel.basic_publish(exchange='queue_name', routing_key='', body=message)
print(' [x] Sent %r' % message)
connection.close()
