from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
import time

# def connectWS():
#     print ('start')
#     ws = websocket_connect('ws://echo.websocket.org/?encoding=text')
#     # print (ws.result())
#     while ws.running():
#         time.sleep(1)
#         print('waiting')
#     print (ws.done())
#     if ws.done():
#         ws.write_message('hello')
#         print ('sent')
#     response = ws.read_message()
#     print (type(response))
#
# for i in range(1):
#     print ('woala')
#     connectWS()

class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        # PeriodicCallback(self.keep_alive, 20000, io_loop=self.ioloop).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print ("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception:
            print ("connection error")
        else:
            print ("connected")
            # self.run()
            # for i in range(1):
            self.sendMessage()
            # print ('trying to send')
            # self.ws.write_message('hello')
            # print ('sent hello')
            # response=yield self.ws.read_message()
            # print (response)
            # time.sleep(5)
            # self.closeconn()

    @gen.coroutine
    def sendMessage(self):
        try:
            print ('trying to send')
            self.ws.write_message('hello')
        # print (self.ws)
            print ('sent hello')
            response=yield self.ws.read_message()
            # time.sleep(1)
            print (response)
        except Exception:
            print ('sent error')
        else:
            self.closeconn()
    #     print ('trying to send')
    #     self.ws.write_message('hello')
    # # print (self.ws)
    #     print ('sent hello')
    #     # time.sleep(1)
    #     # response=yield self.ws.read_message()
    #     # # time.sleep(1)
    #     # print (response)
    #     while True:
    #         print (1)
    #         response = yield self.ws.read_message()
    #         if response is None:
    #             print ('none')
    #             break
    #         print (response)

    @gen.coroutine
    def checkResult(self,result):
        pass


    @gen.coroutine
    def closeconn(self):
        print ('closing')
        self.ws.close()
        print ('closed')
        self.ioloop.stop()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print ("connection closed")
                self.ws = None
                break

if __name__ == "__main__":
    client = Client("wss://uat-lc.mymm.com:7600", 5)
