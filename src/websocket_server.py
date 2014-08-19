
import socket, hashlib, base64, threading, subprocess, sys
from src.KThread import KThread
from config.config_constants import CONTROLLER_PATH
from time import sleep
from subprocess import Popen, STDOUT, PIPE


class PyWSock:
    MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
                "Upgrade: websocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Accept: %s\r\n" + \
                "\r\n"
    LOCK = threading.Lock()

    clients = []

    def __init__(self, console_app):
        self.console_app = console_app

    def recv_data (self, client):
        # as a simple server, we expect to receive:
        #    - all data at one go and one frame
        #    - one frame at a time
        #    - text protocol
        #    - no ping pong messages
        data = bytearray(client.recv(512))
        if(len(data) < 6):
            raise Exception("Error reading data")
        # FIN bit must be set to indicate end of frame
        assert(0x1 == (0xFF & data[0]) >> 7)
        # data must be a text frame
        # 0x8 (close connection) is handled with assertion failure
        assert(0x1 == (0xF & data[0]))

        # assert that data is masked
        assert(0x1 == (0xFF & data[1]) >> 7)
        datalen = (0x7F & data[1])

        #print("received data len %d" %(datalen,))

        str_data = ''
        if(datalen > 0):
            mask_key = data[2:6]
            masked_data = data[6:(6+datalen)]
            unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
            str_data = str(bytearray(unmasked_data))
        return str_data

    def broadcast_resp(self, data):
        # 1st byte: fin bit set. text frame bits set.
        # 2nd byte: no mask. length set in 1 byte.
        resp = bytearray([0b10000001, len(data)])
        # append the data bytes
        for d in bytearray(data):
            resp.append(d)

        self.LOCK.acquire()
        for client in self.clients:
            try:
                client.send(resp)
            except:
                print("error sending to a client")
        self.LOCK.release()

    def parse_headers (self, data):
        headers = {}
        lines = data.splitlines()
        for l in lines:
            parts = l.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        headers['code'] = lines[len(lines) - 1]
        return headers

    def handshake (self, client):
        print('Handshaking...')
        data = client.recv(2048)
        headers = self.parse_headers(data)
        #print('Got headers:')
        #for k, v in headers.iteritems():
        #    print k, ':', v

        key = headers['Sec-WebSocket-Key']
        resp_data = self.HSHAKE_RESP % ((base64.b64encode(hashlib.sha1(key+self.MAGIC).digest()),))
        #print('Response: [%s]' % (resp_data,))
        return client.send(resp_data)

    def handle_client_v2 (self, client, addr):
        self.handshake(client)

        #file_name = 'graph.txt'
        #controller_cmd = sys.prefix + '/bin/python main.py \'' + file_name + '\''
        #print controller_cmd
        #self.console_proc = subprocess.Popen(controller_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        #self.console_thread = KThread(target=self.console_thread_func, args=(client,))
        #self.console_thread.setDaemon(True)
        #self.console_thread.start()

        try:
            while 1:
                data = self.recv_data(client)
                print("received [%s]" % (data,))
                if data[0] == "this_is_input_json":
                    #file_name = 'graph.txt'
                    #controller_cmd = sys.prefix + '/bin/python main.py \'' + file_name + '\''
                    #print controller_cmd
                    #self.console_proc = subprocess.Popen(controller_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                    #self.console_thread = KThread(target=self.console_thread_func, args=(client,))
                    #self.console_thread.setDaemon(True)
                    #self.console_thread.start()
                    self.console_proc.stdin.write(data + '\n')

        except Exception as e:
            print("Exception %s" % (str(e)))
        print('Client closed: ' + str(addr))
        self.LOCK.acquire()
        self.clients.remove(client)
        self.LOCK.release()
        client.close()


    def console_thread_func(self, sock):
        while True:
            out = self.console_proc.stdout.read(1)
            if not out:
                break
            else:
                print out,
                resp = bytearray([0b10000001, len(out)])
                # append the data bytes
                for d in bytearray(out):
                    resp.append(d)
                self.LOCK.acquire()
                for client in self.clients:
                    try:
                        client.send(resp)
                    except:
                        print("error sending to a client")
                self.LOCK.release()
            #self.controller_proc.wait()



    def handle_client (self, client, addr):
        self.handshake(client)
        try:
            while 1:
                data = self.recv_data(client)
                print("received [%s]" % (data,))
                self.broadcast_resp(data)
        except Exception as e:
            print("Exception %s" % (str(e)))
        print('Client closed: ' + str(addr))
        self.LOCK.acquire()
        self.clients.remove(client)
        self.LOCK.release()
        client.close()

    def close_process(self, p):
        p.stdin.close()
        p.stdout.close()

    def start_server (self, port):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(5)
        while(1):
            print ('Waiting for connection...')
            conn, addr = s.accept()
            print ('Connection from: ' + str(addr))
            threading.Thread(target = self.handle_client_v2, args = (conn, addr)).start()
            self.LOCK.acquire()
            self.clients.append(conn)
            self.LOCK.release()

#ws = PyWSock()
#ws.start_server(4545)
