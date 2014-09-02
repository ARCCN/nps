import sys
import sqlite3 as lite
import threading
import os

from scapy.all import *




def catch_sasser_worm_on_host(intf_name):
    # sniff(iface=intf_name, filter="tcp and ( port 445 )", count=1254)
    # sniff(iface=intf_name, filter="tcp and ( port 445 or port 9996 )", count=2*586)
    # sniff(iface=intf_name, filter="tcp and ( port 5554 or port 1033 )", count=2*1)
    sniff(iface=intf_name, count=1000)
    pass


def write_to_file(host_intf_name, infected_hosts_filename):
    file = open(infected_hosts_filename, "a")

    cmd = "ifconfig " + host_intf_name + " | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'" \
                                    ">> " + infected_hosts_filename

    myip = os.popen(cmd).read()
    if myip == '':
        myip = 'NONE'
    print host_intf_name + ':' + myip
    file.write(host_intf_name + ':' + myip)
    file.close()


def write_to_db(host_intf_name, db_filename):
    con = lite.connect(db_filename)

    cur = con.cursor()

    cmd = "ifconfig " + host_intf_name + " | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
    myip = os.popen(cmd).read()
    if myip == '':
        myip = 'NONE'

    cur.execute("INSERT INTO Infected_hosts VALUES('" + host_intf_name + "','" + myip + "')")
    con.commit()
    con.close()



def sniffer(host_intf_name, infected_hosts_filename):
    catch_sasser_worm_on_host(host_intf_name)
    print('Catched!')
    #write_to_file(host_intf_name, infected_hosts_filename)
    write_to_db(host_intf_name, infected_hosts_filename)

    cmd = 'python /home/clusternode/MininetScripts/worm_instance.py ' + host_intf_name + ' &'
    os.popen(cmd)





if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print 'args: (host_intf_name, infected_hosts_db_filename)'
        exit(-1)

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print 'Tesing mode'
        write_to_db("vboxnet0", "/Users/vitalyantonenko/PycharmProjects/NPS/tmp/infected_hosts.db")
        exit(-1)

    if len(sys.argv) != 3:
        print('Not enough args')
        exit(-123)

    host_intf_name = sys.argv[1]
    infected_hosts_db = sys.argv[2]


    sniffer(host_intf_name, infected_hosts_db)



    #write_to_db(host_intf_name, infected_hosts_filename)

