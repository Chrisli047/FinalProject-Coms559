import datetime
import json
import re
import time

import boto3 as boto3

s3 = boto3.client('s3')


def analyse_app_logs():
    response = s3.get_object(Bucket='project-coms559-app-log', Key='logs.json')
    content = response['Body']
    json_content = json.loads(content.read())

    # print(json_content['data'])
    logs = json_content['data']
    counter_book = dict()

    current_time = datetime.datetime.now()
    last_min = current_time - datetime.timedelta(hours=24)

    logs.reverse()
    for log in logs:
        timestamp = log['timestamp']
        dt_object = datetime.datetime.fromtimestamp(timestamp / 1000.0)

        if dt_object > last_min:
            # print(dt_object)
            pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            source_ip = pattern.search(log['message'])[0]
            if source_ip in counter_book:
                counter_book[source_ip] += 1
            else:
                counter_book[source_ip] = 1

            if counter_book[source_ip] > 500:
                print(f"Found the malicious user {source_ip}!")
                f = open("/Users/xiyaoli/Desktop/Study/homework/coms559/FinalProject-Coms559/block_list.json")

                data = json.load(f)
                # print(data)
                if source_ip not in data['malicious_ip_list']:
                    data['malicious_ip_list'].append(source_ip)

                with open("/Users/xiyaoli/Desktop/Study/homework/coms559/FinalProject-Coms559/block_list.json", "w") as outfile:
                    json.dump(data, outfile)
                break
        else:
            # print(f"No malicious attacker has been found day!")
            break
    print("Http calls in a day:")
    print(counter_book)

    # print(f"No malicious attacker has been found day!")
    with open("app_logs.json", "w") as outfile:
        json.dump(json_content, outfile)
    # with open("app_log.json", "w") as outfile:
    #     outfile.write(log_content)
    pass


if __name__ == '__main__':
    print("Start to analyse webserver's daily log...")
    # while True:
    analyse_app_logs()
    # time.sleep(10*60)