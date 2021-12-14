import pendulum
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

local_tz = pendulum.timezone('Asia/Seoul')
now = datetime.now(tz=local_tz)


def print_start_notice():
    print("start")
    return "start!"


def dashin_price_kosdaq():
    import json
    import requests
    import pika

    queue_kosdaq = 'dashin_price'
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.100.1.126'
        , port=5672
        , virtual_host='/'
        , credentials=pika.PlainCredentials('admin', 'admin')
    ))
    channel = connection.channel()
    now_date = datetime.today().weekday()

    if now_date <= 5:
        channel.basic_publish(exchange='', routing_key=queue_kosdaq, body='시작')


def dashin_price_kospi():
    import json
    import requests
    import pika

    queue_kospi = 'dashin_price_2'
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.100.1.126'
        , port=5672
        , virtual_host='/'
        , credentials=pika.PlainCredentials('admin', 'admin')
    ))
    channel = connection.channel()
    now_date = datetime.today().weekday()

    if now_date <= 5:
        channel.basic_publish(exchange='', routing_key=queue_kospi, body='시작')


def print_end_notice():
    print("end")
    return "end!"


# DAG 설정
dag = DAG(
    dag_id='dashin_price_change',
    start_date=datetime(2021, 12, 13, tzinfo=local_tz),
    # schedule_interval = '* * */3 * *'
    schedule_interval='40 15 * * *'
    # 초 분 시간 달 연도
)

# DAG Task 작성
print_start_notice = PythonOperator(
    task_id='print_start_notice',
    # python_callable param points to the function you want to run
    python_callable=print_start_notice,
    # dag param points to the DAG that this task is a part of
    dag=dag
)

dashin_price_kosdaq = PythonOperator(
    task_id='dashin_price_kosdaq',
    python_callable=dashin_price_kosdaq,
    dag=dag
)
dashin_price_kospi = PythonOperator(
    task_id='dashin_price_kospi',
    python_callable=dashin_price_kospi,
    dag=dag
)

print_end_notice = PythonOperator(
    task_id='print_end_notice',
    python_callable=print_end_notice,
    dag=dag
)

# Assign the order of the tasks in our DAG
print_start_notice >> [dashin_price_kosdaq, dashin_price_kospi] >> print_end_notice