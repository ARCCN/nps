__author__ = 'root'

from scapy.all import *
import sys


data = 'payload'
magic = 100

def gen_sasser_traffic( dst_ip, out_intf ):
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=445        ), iface=out_intf, count=1254)
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=[445,9996] ), iface=out_intf, count=586+magic)
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=[5554,1033]), iface=out_intf, count=1+magic)

def gen_blaster_traffic( dst_ip, output_interface ):
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=135        ), iface=output_interface, count=540)
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=[135,4444] ), iface=output_interface, count=2)
    sendp(Ether()/IP(dst=dst_ip)/UDP(dport=69         ), iface=output_interface, count=1)

def gen_welchia_traffic( dst_ip, output_interface ):
    sendp(Ether()/IP(dst=dst_ip)/UDP(dport=53          ), iface=output_interface, count=1)
    sendp(Ether()/IP(dst=dst_ip)/ICMP(                 ), iface=output_interface, count=4434)
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=135         ), iface=output_interface, count=4434)
    sendp(Ether()/IP(dst=dst_ip)/TCP(dport=707         ), iface=output_interface, count=1)
    sendp(Ether()/IP(dst=dst_ip)/UDP(dport=69          ), iface=output_interface, count=1)


if __name__ == "__main__":

    gen_sasser_traffic(sys.argv[1], sys.argv[2])
    print("finish_script")
