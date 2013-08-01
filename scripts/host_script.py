__author__ = 'root'

import sys
from scapy.all import *
import threading


MALWARE_CENTER_IP   = "1.2.1.1"
MALWARE_CENTER_PORT = 56565

OVERLOAD_STATE_KOEF = 70


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

class Domain:
    def __init__(self, id, host_num, sv, iv, res):
        self.id = int(id)
        self.host_num = int(host_num)
        self.sv = sv
        self.iv = iv
        self.res = float(res)

        self.queue_links = {} # queue for each link connected for this domain
        self.link_source_domain = {}
        self.load = float(0)
        self.res_flow_dist = {}
        self.overload_state = False
        self.infectivity_koef = 0.5

    def add_load(self, f_id, added_load, prev_domain_id = None):

        overload = float(0)
        if (self.load + added_load) > self.res:
            self.overload_state = True
            overload = self.load + added_load - self.res
            self.load = self.res
        else:
            self.load += added_load

        if f_id in self.res_flow_dist:
            self.res_flow_dist[f_id] += added_load - overload
        else:
            self.res_flow_dist[f_id] = float(0)
            self.res_flow_dist[f_id] += added_load - overload

        #    if prev_domain_id is not None:
        #        l_id = self.link_source_domain[prev_domain_id]
        #        self.queue_links[l_id] += added_load - overload
        return overload

    def sub_load(self, f_id, subbed_load, prev_domain_id = None):
        if self.load <= subbed_load:
            self.load = float(0)
            self.res_flow_dist[f_id] = float(0)
        else:
            self.load -= subbed_load
            self.res_flow_dist[f_id] -= subbed_load

        if self.load/self.res < OVERLOAD_STATE_KOEF/100:
            self.overload_state = False

        #    if prev_domain_id is not None:
        #      l_id = self.link_source_domain[prev_domain_id]
        #      self.queue_links[l_id] += subbed_load - minus_load

    def change_inf_hosts_num(self, mal_id, transfer_rate, copy_size, inf_speed):
        vuln_hosts_num = int(self.host_num * (1 - self.sv[mal_id]) - self.iv[mal_id])

        result_inf_hosts_speed = int((self.iv[mal_id] + (transfer_rate/copy_size)) * inf_speed * vuln_hosts_num \
                                     / self.host_num * self.infectivity_koef
        )

        if vuln_hosts_num < result_inf_hosts_speed:
            self.iv[mal_id] += vuln_hosts_num
        else:
            self.iv[mal_id] += result_inf_hosts_speed

    def get_malware_info_string(self, malware_id):
        return "M=" + str(malware_id) + " " + str(int(self.iv[malware_id])) + "/" + str(self.host_num)

    def get_overload_state(self):
        return self.overload_state

    def print_config(self):
        print("ID =", self.id)
        print("HOSTS NUMBER =", self.host_num)
        print("SV =", self.sv)
        print("IV =", self.iv)
        print("RES =", self.res)



if __name__ == '__main__':
    host_ip = sys.argv[1]
    # intf_name = sys.argv[2]
    thread = threading.Thread(target=sniffer, args=(host_ip,))
    thread.start()

    domain = Domain(1,100,[1,2,2],[1,1,1],1000)
    domain.print_config()