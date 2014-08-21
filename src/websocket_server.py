# import the libraries
import tornado.web
import tornado.websocket
import tornado.ioloop
import sys, subprocess, os
from src.KThread import KThread
from main import NPS

from config.config_constants import WEB_SOCKET_SERVER_PORT, MSGEXCH_SERVER_IP, \
    MSGEXCH_SERVER_PORT, MSGEXCH_SERVER_PATH, CONTROLLER_PATH



# This is our WebSocketHandler - it handles the messages
# from the tornado server
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # the client connected
    def open(self):
        print "New client connected"
        if os.path.isfile("tmp/groups.txt"):
            os.remove("tmp/groups.txt")
        self.write_message("You are connected\n")


    # the client sent the message
    def on_message(self, message):
        print message
        if message.find('msg::input_json::') == 0:
            json_data = message[len('msg::input_json::'):]
            print json_data
            self.write_message('Recieved JSON\n')
            self.input_json_file_name = 'input_json.txt'
            file_ = open(self.input_json_file_name, 'w')
            file_.write(json_data)
            file_.write('\n')
            file_.close()
            self.write_message('Saved JSON to file ' + self.input_json_file_name + '\n')

        elif message.find('msg::simulate::') == 0:
            console_cmd = sys.prefix + '/bin/python main.py \'' + self.input_json_file_name + '\''
            print console_cmd
            self.console_proc = subprocess.Popen(console_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            self.console_mon_thread = KThread(target=self.console_mon_thread_func)
            self.console_mon_thread.setDaemon(True)
            self.console_mon_thread.start()

        elif message.find('msg::controller::') == 0:
            controller_cmd = "java -jar " + CONTROLLER_PATH + "/target/floodlight.jar"
            print controller_cmd
            self.controller_proc = subprocess.Popen(controller_cmd, stdout=subprocess.PIPE, shell=True)
            self.controller_mon_thread = KThread(target=self.controller_mon_thread_func)
            self.controller_mon_thread.setDaemon(True)
            self.controller_mon_thread.start()

        elif message.find('msg::groups::') == 0:
            file_ = open('tmp/groups.txt', 'r')
            groups = file_.readline()
            file_.close()
            self.write_message('msg::groups::' + groups)
        else:
            self.console_proc.stdin.write(message + '\n')


    def console_mon_thread_func(self):
        while True:
            out = self.console_proc.stdout.read(1)
            #self.console_proc.stdout.flush()
            if not out:
                break
            else:
                #print out,
                self.write_message(out)

    def controller_mon_thread_func(self):
        while True:
            out = self.controller_proc.stdout.readline()
            if not out:
                break
            else:
                #print out,
                self.write_message("msg::controller::" + out)


    # client disconnected
    def on_close(self):
        print "Client disconnected"
        
        
class WSServer:
    def __init__(self):
        self.application = tornado.web.Application([
            (r"/", WebSocketHandler),
        ])
    
    def start(self):
        self.application.listen(WEB_SOCKET_SERVER_PORT)
        tornado.ioloop.IOLoop.instance().start()