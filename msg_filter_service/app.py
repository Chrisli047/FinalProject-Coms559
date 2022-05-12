import json

import boto3 as boto3
from flask import Flask, request

app = Flask(__name__)
s3 = boto3.client('s3')


@app.route('/msg/vpc', methods=['POST'])
def msg_vpc():
    logs = request.json
    # print(logs)
    update_s3_vpc_log(logs['data'])

    return 'Done'


@app.route('/msg/app', methods=['POST'])
def msg_app():
    logs = request.json
    # print(logs)
    update_s3_app_log(logs['data'])
    return 'Done'


def update_s3_app_log(data):
    response = s3.get_object(Bucket='project-coms559-app-log', Key='logs.json')
    content = response['Body']
    json_content = json.loads(content.read())
    json_content['data'] = json_content['data'] + data

    s3.put_object(
        Body=json.dumps(json_content),
        Bucket='project-coms559-app-log',
        Key='logs.json'
    )
    print("Logs from webserver has been updated to S3 storage.")


def update_s3_vpc_log(data):
    response = s3.get_object(Bucket='project-coms559-vpc-log', Key='logs.json')
    content = response['Body']
    json_content = json.loads(content.read())
    json_content['data'] = json_content['data'] + data

    s3.put_object(
        Body=json.dumps(json_content),
        Bucket='project-coms559-vpc-log',
        Key='logs.json'
    )
    print("Logs from vpc has been updated to S3 storage.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
