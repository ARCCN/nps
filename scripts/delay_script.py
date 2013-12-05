__author__ = 'vitalyantonenko'

import os

def test_delay(dst_IP, threshold):
    delay = os.popen("ping -c 1 " + dst_IP + " | tail -1 | awk '{print $4}' | awk -F'/' '{print $3}'").read()

    if float(delay)/2 <= threshold: # cos it is RTT
        print('GOOD!')
    else:
        print('DROP PACKET!')


if __name__ == '__main__':
    print('Hello, We will test Delay script')

    test_delay('8.8.8.8', 10)
    test_delay('8.8.8.8', 20)


