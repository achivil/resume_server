import os
import socket
import time
import json

SEND_PACE = 2097152

order_header = json.dumps(['SENDSTART', 'test1'])
#order = json.dumps({'movie1.png': 476797-00, 'VTS_02_1.png': 118812-00})
#order1 = json.dumps(['FILE', {'filename':  'movie1.png', 'filesize': 476797, 'filemd5': 'xx1'}])
#order2 = json.dumps(['FILE', {'filename':'VTS_02_1.png', 'filesize': 118812, 'filemd5': '001xx2'}])
order2 = json.dumps(['FILE', {'filename':'movie.mp4', 'filesize': 390390859, 'filemd5': '001xx3'}])
order_end = json.dumps(['SENDEND'])


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('order')
orderlist = [order_header, order2, order_end]
new_orderlist = []
for o in orderlist:
    s.send(o)
    time.sleep(0.1)
data = s.recv(1024)
time.sleep(0.1)
print data
print 'received %s bytes' % len(data)
if 'No file' in data:
    print data
    s.close()
    exit()
#data = s.recv(128)
#time.sleep(1)
#new_orderlist = json.loads(data)
new_orderlist = json.loads(data)
print new_orderlist
for fileinfo in new_orderlist:
    print fileinfo[0]
    filename = fileinfo[0]
    filepath = os.path.join("/Users/achivil/work/upload/upload/tmpfile", filename)
    print filepath
    with open(filepath, 'rb') as f:
    #f = open(filepath, 'rb')
        if fileinfo[2] != 0:
            print fileinfo[2] * SEND_PACE
            f.seek(fileinfo[2] * SEND_PACE)
        while 1:
            time.sleep(0.1)
            data = f.read(SEND_PACE)
            #print "get file"
            if not data:
                break
            s.send(data)
        print "send over"
    #f.close()
s.close()
