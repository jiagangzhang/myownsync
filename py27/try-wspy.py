# encoding: utf-8

import wspy
import ssl
from wspy.deflate_message import DeflateMessage
from wspy.message import create_message
import zlib
		
Ext=DeflateMessage()
Ext.request={'client_max_window_bits': zlib.MAX_WBITS,
        'client_no_context_takeover': False}

class NewClient(wspy.Connection):
	pass

# def deflate(data):
# 	defl=zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION,
#                         zlib.DEFLATED, zlib.MAX_WBITS)
# 	compressed = defl.compress(data)
# 	compressed += defl.flush(zlib.Z_SYNC_FLUSH)
# 	assert compressed[-4:] == '\x00\x00\xff\xff'
# 	return compressed[:-4]

sock=wspy.websocket(origin='https://www.websocket.org',extensions=[Ext])
sock.enable_ssl()
sock.connect(('mobile-mm.eastasia.cloudapp.azure.com',7600))
# sock.connect(('echo.websocket.org',80))
# sock.send(wspy.Frame(wspy.OPCODE_TEXT,'hello'))
# response=sock.recv()
# print response

conn=NewClient(sock)
# conn.send(wspy.TextMessage('hello'))

paylo='''{
  "Type": "Announce",
  "SenderUserKey": "0e152fb4-ed0f-11e6-a1fc-acbc32d426e5",
  "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIwZTE1MmZiNC1lZDBmLTExZTYtYTFmYy1hY2JjMzJkNDI2ZTUiLCJVc2VyS2V5IjoiMGUxNTJmYjQtZWQwZi0xMWU2LWExZmMtYWNiYzMyZDQyNmU1IiwiaWF0IjoxNDg2Njk4Nzc2LCJleHAiOjE0ODkyOTA3NzZ9.8V9YTCZtqq43H8oS4zXQixrS9zVUB_hBe49hgwpW2BY",
  "CorrelationKey": "78c963e0-3183-43c7-8dbe-6692e32bcd45"
}'''
# sock.send(wspy.Frame(wspy.OPCODE_TEXT, paylo ,mask=True,rsv1=True))

# msg=wspy.Frame(wspy.OPCODE_TEXT, deflate(paylo) ,mask=True, rsv1=True)
# print repr(msg.payload)
# sock.send(msg)
# sock.send(wspy.Frame(wspy.OPCODE_TEXT, deflate(paylo) ,mask=True, rsv1=True))
# print wspy.Frame(wspy.OPCODE_TEXT, paylo ,mask=True, rsv1=True).rsv1
msg=create_message(0x1,paylo)
# print msg
conn.send(msg,mask=True)
print 'sent announce'
response1=conn.recv()
response2=conn.recv()
# print response
# print response1
# print response2
# print type(response2)
# print response2.payload

paylo='''{
  "Type": "ConvStart",
  "ConvType": "Private",
  "Queue": "General",
  "UserList": [
    {
      "UserKey": "0e152fb4-ed0f-11e6-a1fc-acbc32d426e5",
      "MerchantId": null
    },
    {
      "UserKey": "b0d268dc-ed11-11e6-a1fc-acbc32d426e5",
      "MerchantId": null
    }
  ],
  "SenderUserKey": "0e152fb4-ed0f-11e6-a1fc-acbc32d426e5",
  "SenderMerchantId": null,
  "CorrelationKey": "96292c1d-6106-4b8c-9dcb-60a8e3fa22c9"
}
'''
msg=create_message(0x1,paylo)
# print msg
conn.send(msg,mask=True)
print 'sent start'
response1=conn.recv()
response2=conn.recv()
print response1.payload
print response2.payload
print 'closing'
conn.close(reason='close')