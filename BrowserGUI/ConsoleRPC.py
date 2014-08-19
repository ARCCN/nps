import zerorpc

class HelloRPC(object):
    def hello(self, name):
        print "Hello, %s" % name
        return "Hello, %s" % name

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()