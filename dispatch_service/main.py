import time
import threading

import boto3
import datetime
import requests
import json

AWS_REGION = "us-east-2"

client = boto3.client('logs', region_name=AWS_REGION)


def read_vpc_logs():
    print("Reading vpc logs from cloud watch...")
    current_time = datetime.datetime.now()
    last_min = current_time - datetime.timedelta(minutes=5)

    while True:
        print("Start time of the part of the VPC log: ")
        print(last_min)
        print("End time of the part of the VPC log: ")
        print(current_time)

        response = client.get_log_events(
            logGroupName='project-coms559-cloudwatch',
            logStreamName='eni-069065b9efb756a11-all',
            startTime=int(last_min.strftime('%s')) * 1000,
            endTime=int(current_time.strftime('%s')) * 1000,
            limit=200,
            startFromHead=True
        )

        log_events = response['events']
        logs = {
            'data': log_events
        }

        send_to_filter(logs, 'vpc')
        send_to_analyse(logs, 'vpc')

        # for each_event in log_events:
        #     print(each_event)

        last_min = current_time
        current_time = last_min + datetime.timedelta(minutes=5)
        time.sleep(305)


def read_app_logs():
    print("Reading app logs from cloud watch...")
    current_time = datetime.datetime.now()
    last_min = current_time - datetime.timedelta(minutes=5)

    while True:
        print("Start time of the part of the APP log: ")
        print(last_min)
        print("End time of the part of the APP log: ")
        print(current_time)

        response = client.describe_log_streams(
            logGroupName='watchtower',
            orderBy='LastEventTime',
            descending=True,
            limit=50
        )

        latest_log_stream = response['logStreams'][0]['logStreamName']
        print(latest_log_stream)

        log_content = client.get_log_events(
            logGroupName='watchtower',
            logStreamName=latest_log_stream,
            startTime=int(last_min.strftime('%s')) * 1000,
            endTime=int(current_time.strftime('%s')) * 1000,
            limit=200,
        )
        # Serializing json
        # json_object = json.dumps(log_content, indent=4)
        log_events = log_content['events']
        logs = {
            'data': log_events
        }

        send_to_filter(logs, 'app')
        send_to_analyse(logs, 'app')

        # with open("app_log.json", "w") as outfile:
        #     outfile.write(log_content)

        # log_events = response['events']
        # logs = {
        #     'data': log_events
        # }
        #
        # send_to_filter(logs)
        # send_to_analyse(logs)

        # for each_event in log_events:
        #     print(each_event)

        last_min = current_time
        current_time = last_min + datetime.timedelta(minutes=5)
        time.sleep(305)


def send_to_analyse(logs, log_type):
    if log_type == 'vpc':
        r = requests.post('http://localhost:5002/analyse/vpc', json=logs)
    if log_type == 'app':
        r = requests.post('http://localhost:5002/analyse/app', json=logs)

    if r.status_code == 200:
        print(log_type + ' logs has been sent to analyse server')
    else:
        print(log_type + ' logs failed to sent to analyse server')
    pass


def send_to_filter(logs, log_type):
    if log_type == 'vpc':
        r = requests.post('http://localhost:5003/msg/vpc', json=logs)
    if log_type == 'app':
        r = requests.post('http://localhost:5003/msg/app', json=logs)

    if r.status_code == 200:
        print(log_type + ' logs has been sent to msg filter server')
    else:
        print(log_type + ' logs failed to sent to msg filter server')
    pass


if __name__ == '__main__':
    t1 = threading.Thread(target=read_vpc_logs)
    t2 = threading.Thread(target=read_app_logs)

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()


    while 1:
        pass