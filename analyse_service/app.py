import re

from flask import Flask, request
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)


def send_email(msg):
    mail_content = "Alert!!! " + msg
    # The mail addresses and password
    sender_address = 'sender_email'
    sender_pass = 'Password'
    receiver_address = 'admin_email'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Security attack alert!!!'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Alert mail has been sent out to the administrator')


def analyse_port_scanner(data):
    # f = open('Raw_data.json')
    logs = data['data']
    suspicious_pool = {0}

    for log in logs:
        log_attrs = log['message'].split(' ')
        # if log_attrs[-2] == 'REJECT':
        #     suspicious_pool.add(log_attrs[6])
        suspicious_pool.add(log_attrs[6])
        if len(suspicious_pool) > 80:
            print("Attack from port scanner detected!")
            send_email("Your vpc is under the attack from the port scanner!!!")
            break
    #     print(log_attrs[6], log_attrs[-2])
    print("Current number of port access: " + str(len(suspicious_pool)))
    # print(logs)


def excessive_call_from_same_ip(data):
    # f = open('app_log.json')
    #
    # data = json.load(f)
    logs = data['data']
    counter_book = dict()

    for log in logs:
        # print(log['message'])
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        source_ip = pattern.search(log['message'])[0]

        f = open("/Users/xiyaoli/Desktop/Study/homework/coms559/FinalProject-Coms559/block_list.json")
        malicious_ip = json.load(f)
        if source_ip in malicious_ip['malicious_ip_list']:
            print(f"Http request form Malicious IP: {source_ip} has arrived !!!")
            send_email(
                f"Http request form Malicious IP: {source_ip} has arrived !!!")
            break

        if source_ip in counter_book:
            counter_book[source_ip] += 1
        else:
            counter_book[source_ip] = 1

        if counter_book[source_ip] > 20:
            send_email(f"Your websever has been unusually called for more than 20 times in last 5 minutes from {source_ip} !!!")
            break

        # print(source_ip)
    print("Http calls in last 5 minutes: ")
    print(counter_book)


@app.route('/analyse/vpc', methods=['POST'])
def analyse_vpc():
    print("Received VPC logs")
    logs = request.json
    # print(logs)
    analyse_port_scanner(logs)

    return 'Done'


@app.route('/analyse/app', methods=['POST'])
def analyse_app():
    print("Received webserver logs")
    logs = request.json
    excessive_call_from_same_ip(logs)

    return 'Done'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
