# from websocket import create_connection
# #ws = create_connection("wss://uat-lc.mymm.com:7600/?,%20deflate,%20sdch,%20br&Accept-Language=zh-CN,zh;q=0.8,en;q=0.6&Cache-Control=no-cache&Connection=Upgrade&Host=uat-lc.mymm.com:7600&Origin=http://uat-lw.mymm.com&Pragma=no-cache&Sec-WebSocket-Extensions=permessage-deflate;%20client_max_window_bits&Sec-WebSocket-Key=7ozsDsj8cD+9uVro7M5q/A==&Sec-WebSocket-Version=13&Upgrade=websocket&User-Agent:=Mozilla/5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_11_4)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/51.0.2704.103%20Safari/537.36")
# print ("Sending 'Hello, World'...")
# ws.send("Hello, World")
# print ("Sent")
# print ("Reeiving...")
# result =  ws.recv()
# print ("Received '%s'" % result)
# ws.close()



import sys

from twisted.internet import reactor
from twisted.python import log

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS

from autobahn.websocket.compress import PerMessageDeflateOffer, \
    PerMessageDeflateResponse, \
    PerMessageDeflateResponseAccept


class EchoClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("WebSocket extensions in use: {}".format(response.extensions))

    def sendHello(self):
        msg = "Hello, world!" * 100
        self.sendMessage(msg.encode('utf8'))

    def onOpen(self):
        self.sendHello()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))
        reactor.callLater(1, self.sendHello)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Need the WebSocket server address, i.e. ws://127.0.0.1:9000")
        sys.exit(1)

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(sys.argv[1])
    factory.protocol = EchoClientProtocol

    # Enable WebSocket extension "permessage-deflate".

    # The extensions offered to the server ..
    offers = [PerMessageDeflateOffer()]
    factory.setProtocolOptions(perMessageCompressionOffers=offers)

    # Function to accept responses from the server ..
    def accept(response):
        if isinstance(response, PerMessageDeflateResponse):
            return PerMessageDeflateResponseAccept(response)

    factory.setProtocolOptions(perMessageCompressionAccept=accept)

    # run client
    connectWS(factory)
    reactor.run()
    # reactor.callFromThread(reactor.stop)
