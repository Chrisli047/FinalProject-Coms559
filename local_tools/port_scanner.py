import threading
import time
import pyfiglet
import sys
import socket
import requests

from datetime import datetime


def port_scanner():
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)


    target = "3.12.148.15"

    # Add Banner
    print("-" * 50)
    print("Scanning Target: " + target)
    print("Scanning started at:" + str(datetime.now()))
    print("-" * 50)

    try:

        # will scan ports between 1 to 65,535
        for port in range(1, 65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # returns an error indicator
            result = s.connect_ex((target, port))
            if result == 0:
                print("Port {} is open".format(port))
            s.close()

    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()


def loop_http_call():
    print("Start loop http call")
    while True:
        response = requests.get("http://3.12.148.15:5000/")
        time.sleep(5)


if __name__ == '__main__':
    # loop_http_call()
    # port_scanner()
    print("Start to mock the attack on VPC and webser running on EC2 instance...")
    t1 = threading.Thread(target=loop_http_call)
    t2 = threading.Thread(target=port_scanner)
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()

    # t1.join()
    # t2.join()

    while 1:
        pass
