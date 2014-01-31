import sys
from scapy.all import *
import threading
import os



def catch_sasser_worm_on_host(intf_name):
    sniff(iface=intf_name, filter="tcp and ( port 445 )", count=1254)
    sniff(iface=intf_name, filter="tcp and ( port 445 or port 9996 )", count=2*586)
    sniff(iface=intf_name, filter="tcp and ( port 5554 or port 1033 )", count=2*1)


def write_to_file_about_infection(host_intf_name, infected_hosts_filename):
    file = open(infected_hosts_filename, "a")

    cmd = "ifconfig " + host_intf_name + " | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'" \
                                    ">> " + infected_hosts_filename

    myip = os.popen(cmd).read()
    file.write(myip)
    file.close()

def sniffer(host_intf_name, infected_hosts_filename):
    catch_sasser_worm_on_host(host_intf_name)
    #print('Catched!')
    write_to_file_about_infection(host_intf_name, infected_hosts_filename)




if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print 'args: (host_intf_name, infected_hosts_filename)'
        exit(-1)

    if len(sys.argv) != 3:
        print('Not enough args')
        exit(-123)

    host_intf_name = sys.argv[1]
    infected_hosts_filename = sys.argv[2]


    #thread = threading.Thread(target=sniffer, args=(host_intf_name, infected_hosts_filename))
    #thread.start()
    sniffer(host_intf_name, infected_hosts_filename)

    #print("finish_script")