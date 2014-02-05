__author__ = 'vitalyantonenko'

from scapy.all import *
from random import choice
import sys
import time

IP_GENERATION_FLAG = False
WORM_PROP_SLEEP = 2
HIT_LIST_SIZE = 33

default_ip_db = ['1.2.3.2', '1.2.3.3', '1.2.3.4', '1.2.3.5', '1.2.3.6', '1.2.3.7', '1.2.3.8']
#ip_db = ['172.0.1.100']

def gen_hit_list(hit_num):
    hit_list = []

    for i in range(hit_num):
        hit_list.append("1.2.3." + str(i+2))
    return hit_list

def gen_sasser_traffic(dst_ip, out_intf):
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=445        ), iface=out_intf, count=1254)
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=[445,9996] ), iface=out_intf, count=586)
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=[5554,1033]), iface=out_intf, count=1)


def worm_activity(out_intf):
    hit_list = gen_hit_list(HIT_LIST_SIZE)
    while True:
        # select IP address of next target
        if not IP_GENERATION_FLAG:
            current_target_ip = choice(hit_list)
            print current_target_ip

        # send its body to target
        gen_sasser_traffic(current_target_ip, out_intf)

        #sleep
        time.sleep(WORM_PROP_SLEEP)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print('args: (out_intf)')
        exit(-1)

    if len(sys.argv) != 2:
        print('Not enough args')
        exit(-123)

    out_intf = sys.argv[1]

    worm_activity(out_intf)




