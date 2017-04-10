only python 2 supported

start venv

git clone https://github.com/jiagangzhang/wspy
cd wspy
python setup.py install



wspy-backup-0406 contains modifications to show sent and received frames, to debug.

details:
	connection.py
		line 90	
			print frame
			print frame.payload
	handshake.py
		line 44
			print raw
			print headers
		line 103
			print hdr
		line 241
			print 'sent headers'
			print 'handled response'
		line 283
			print name,',',accept_params
			for ext in self.wsock.extensions:
                    print ext
                    if name in ext.names:
                        print name
    websocket.py
    	line 131
    		print 'complete connect'
    	line 140
    		print frame