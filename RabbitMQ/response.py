#!/usr/bin/env python
import pika
from pika import credentials

cred = pika.PlainCredentials('user', 'pwd')
connection = pika.BlockingConnection(
  pika.ConnectionParameters(host='host_ip',credentials=cred))
channel = connection.channel()

# channel.exchange_declare(exchange='', exchange_type='fanout')

# result = channel.queue_declare(queue='ebest_trade_response', exclusive=True)
# queue_name = result.method.queue

# channel.queue_bind(exchange='', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
  print(' [x] %r' % body)

channel.basic_consume(
  queue='queue_name', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
