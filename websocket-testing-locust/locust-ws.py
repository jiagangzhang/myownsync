# encoding: utf-8
import time

from locust import TaskSet, task, Locust, events

import wspy
import ssl
from wspy.deflate_message import DeflateMessage
from wspy.message import create_message
import zlib

printTask = True
printError = True

def print_task(arg):
    if printTask : print arg
    elif printError : print arg
    else: pass

Ext=DeflateMessage()
Ext.request={'client_max_window_bits': zlib.MAX_WBITS,
        'client_no_context_takeover': False}
class NewClient(wspy.Connection):
	pass

class WSClient(object):
	"""docstring for WSClient"""
	def __init__(self):
		pass

	def send(self,connection,msg,mask=True,name='Send WebSocket Message'):
		conn=connection
		start_time = time.time()
		try:
			conn.send(msg,mask=mask)
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			events.request_failure.fire(request_type="send", name=name, response_time=total_time, exception=e)
		else:
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type="send", name=name, response_time=total_time, response_length=0)

	def receive(self,connection,name='Receive WebSocket Message'):
		conn=connection
		start_time = time.time()
		try:
			resp=conn.recv()
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			events.request_failure.fire(request_type="receive", name=name, response_time=total_time, exception=e)
		else:
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type="receive", name=name, response_time=total_time, response_length=0)
			return resp.payload

class WSLocust(Locust):
	"""docstring for WSLocust"""
	def __init__(self, *args,**kwargs):
		super(WSLocust, self).__init__(*args,**kwargs)
		self.client=WSClient()

class simple_ws(TaskSet):
	def on_start(self):
		sock=wspy.websocket(origin='https://www.websocket.org',extensions=[Ext])
		sock.enable_ssl()
		sock.connect(('uat-lc.mymm.com',7600))
		self.conn=NewClient(sock)
		paylo='''{
		  "Type": "Announce",
		  "SenderUserKey": "0e152fb4-ed0f-11e6-a1fc-acbc32d426e5",
		  "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIwZTE1MmZiNC1lZDBmLTExZTYtYTFmYy1hY2JjMzJkNDI2ZTUiLCJVc2VyS2V5IjoiMGUxNTJmYjQtZWQwZi0xMWU2LWExZmMtYWNiYzMyZDQyNmU1IiwiaWF0IjoxNDg2Njk4Nzc2LCJleHAiOjE0ODkyOTA3NzZ9.8V9YTCZtqq43H8oS4zXQixrS9zVUB_hBe49hgwpW2BY",
		  "CorrelationKey": "78c963e0-3183-43c7-8dbe-6692e32bcd45"
		}'''
		msg=wspy.message.create_message(0x1,paylo)
		self.client.send(self.conn,msg,mask=True,name='Announce')
		print_task ('sent hello')
		resp1=self.client.receive(self.conn,name='Receive message 1')
		resp2=self.client.receive(self.conn,name='Receive Ack')
		print_task (resp2)
		if 'Announce' in resp2:pass
		else: 
			print 'no announce received'
			self.interrupt()

	@task
	def dummy(self):
		time.sleep(5)
		self.interrupt()

	# @task
	# def Announce(self):
	# 	paylo='''{
	# 	  "Type": "Announce",
	# 	  "SenderUserKey": "0e152fb4-ed0f-11e6-a1fc-acbc32d426e5",
	# 	  "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIwZTE1MmZiNC1lZDBmLTExZTYtYTFmYy1hY2JjMzJkNDI2ZTUiLCJVc2VyS2V5IjoiMGUxNTJmYjQtZWQwZi0xMWU2LWExZmMtYWNiYzMyZDQyNmU1IiwiaWF0IjoxNDg2Njk4Nzc2LCJleHAiOjE0ODkyOTA3NzZ9.8V9YTCZtqq43H8oS4zXQixrS9zVUB_hBe49hgwpW2BY",
	# 	  "CorrelationKey": "78c963e0-3183-43c7-8dbe-6692e32bcd45"
	# 	}'''
	# 	msg=wspy.message.create_message(0x1,paylo)
	# 	# self.conn.send(msg,mask=True)
	# 	self.client.send(self.conn,msg,mask=True,name='Announce')
	# 	print_task ('sent hello')
	# 	# resp1=self.conn.recv()
	# 	# resp2=self.conn.recv()
	# 	resp1=self.client.receive(self.conn,name='Receive message 1')
	# 	resp2=self.client.receive(self.conn,name='Receive Ack')
	# 	print_task (resp2)

class MyTaskSet(TaskSet):
    # tasks={dummy_task:1}
    # tasks={cart_wishlist_WishList:1}
    tasks={simple_ws:1}
		
class MyLocust(WSLocust):
    task_set = MyTaskSet
    print 'woala'
    # host= url
    min_wait = 1000
    max_wait = 5000
		

		