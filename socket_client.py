import socket

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("test")
#s.send('GET / HTTP/1.0\r\n\r\n')
s.send('Send file movie22222.mp4')
data = s.recv(1024)
print 'received %s bytes' % len(data)
print data
s.close()
