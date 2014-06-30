import os
import json
import gevent
from gevent.pywsgi import WSGIServer
from gevent.server import StreamServer
from gevent import socket

from save_file import trans_file, get_order

BUFSIZE = 1024
ORDERSIZE = 512
path = '/Users/achivil/tmpfile'

def app(socket, address):
    checked_order, filepath = get_order(socket)
    print checked_order
    if not checked_order:
        ss = socket.send('No file need send.')
        socket.close()
        return
    ss = socket.send(json.dumps(checked_order))
    for file in checked_order:
        status = trans_file(socket, os.path.join(filepath, file[0]), file[1], file[2])
        print status
    socket.close()
    return
##############################
"""
    name = []
    rr = socket.recv(ORDERSIZE)
    if rr:
        order = json.loads(rr)
        print order[0]
        filepath = os.path.join(path, order[0])
        fileinfo = order[1]
        for n in fileinfo.keys():
            print n
            if os.path.isfile(os.path.join(filepath, n)):
                del fileinfo[n]
        name = fileinfo.keys()
        filesize = fileinfo.values()
        if name and filesize:
            print name
            print filesize
            #ss = socket.send('Ready to Savefile.')
            ss = socket.send(json.dumps(order))
            i = 0
            for i in range(len(name)):
                status = trans_file(socket, os.path.join(filepath, name[i]), filesize[i])
                print status
        else:
            ss = socket.send('No file need send.')
    #if status == 1:
        #socket.send("Finish sending")
    socket.close()
    return
"""
#####################################
"""
def trans_file(socket, filename, filesize):
    #filename = os.path.join(filepath, name)
    f = open_file(filename)
    if f == 0:
        print "Open file failed"
        return 3
    buff = ""
    count = 0
    restsize = filesize
    while 1:
        if restsize > BUFSIZE:
            filedata = socket.recv(BUFSIZE)
        else:
            filedata = socket.recv(restsize)
        if not filedata:
            break
        f.write(filedata)
        restsize = restsize - len(filedata)
        if restsize == 0:
            break
    f.close()
    return 1
"""

if __name__ == "__main__":
    try:
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    except socket.error, e:
        raise "socket error"
    sockname = 'order'
    if os.path.exists(sockname):
        os.remove(sockname)
    listener.bind(sockname)
    listener.listen(1)
    StreamServer(listener, app).serve_forever()
    #WSGIserver(listener, app).serve_forever()
