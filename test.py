# import the libraries
import tornado.web
import tornado.websocket
import tornado.ioloop
import sys, subprocess
from src.KThread import KThread



# This is our WebSocketHandler - it handles the messages
# from the tornado server
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # the client connected
    def open(self):
        print "New client connected"
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
            self.console_thread = KThread(target=self.console_thread_func)
            self.console_thread.setDaemon(True)
            self.console_thread.start()
        else:
            self.console_proc.stdin.write(message + '\n')


    def console_thread_func(self):
        while True:
            out = self.console_proc.stdout.read(1)
            if not out:
                break
            else:
                print out,
                self.write_message(out)


    # client disconnected
    def on_close(self):
        print "Client disconnected"

# start a new WebSocket Application
# use "/" as the root, and the 
# WebSocketHandler as our handler
application = tornado.web.Application([
    (r"/", WebSocketHandler),
])

# start the tornado server on port 8888
if __name__ == "__main__":
    application.listen(9876)
    tornado.ioloop.IOLoop.instance().start()

