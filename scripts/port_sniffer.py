import sys
from scapy.all import *
import threading


MALWARE_CENTER_IP   = "1.2.1.1"
MALWARE_CENTER_PORT = 56565

def catch_sasser_worm_on_host(intf_name):
    sniff(iface=intf_name, filter="tcp and ( port 445 )", count=1254)
    sniff(iface=intf_name, filter="tcp and ( port 445 or port 9996 )", count=2*586)
    sniff(iface=intf_name, filter="tcp and ( port 5554 or port 1033 )", count=2*1)

def tell_malware_center_about_infection(ip="localhost", port=56565, message="infected"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message,(ip,port))
        print("send worm instance complete")
    finally:
        sock.close()

def sniffer(host_ip):
    print(host_ip)
    #    catch_sasser_worm_on_host(int_name)
    tell_malware_center_about_infection(MALWARE_CENTER_IP, MALWARE_CENTER_PORT, host_ip)


if __name__=="__main__":
    host_ip = sys.argv[1]
    # intf_name = sys.argv[2]
    thread = threading.Thread(target=sniffer, args=(host_ip,))
    thread.start()

    print("finish_script")