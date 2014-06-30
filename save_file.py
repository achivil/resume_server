import os
import socket
import json
import math

path = '/Users/achivil/tmpfile'
BUFSIZE = 1024
ORDERSIZE = 512
SEND_PACE = 2097152

"""
def open_file(filename):
    #f = open(filename, 'a+')
    f = open(filename, 'a+')
    if f:
        return f
    else:
        return 0
"""

def get_order(socket):
    fileinfo = []
    while 1:
        rr = socket.recv(ORDERSIZE)
        if rr:
            order = json.loads(rr)
            #if 'SENDSTART' in order:
            if 'SENDEND' in order[0]:
                break
            elif 'SENDSTART' in order[0]:
                filepath = os.path.join(path, order[1])
                continue
            else:
                fileinfo.append(order)
    new_fileinfo = check_file(fileinfo, filepath)
    return new_fileinfo, filepath
    #new_fileinfo = check_file(fileinfo, filepath)
    #return new_fileinfo, filepath


def check_file(fileinfo, filepath):
    i = 0
    status = 0
    new_fileinfo = []
    for i in range(len(fileinfo)-1, -1, -1):
        filename, filesize, filemd5 = fileinfo[i][1]['filename'], fileinfo[i][1]['filesize'], fileinfo[i][1]['filemd5']
        tempfile = os.path.join(filepath, filename)
        if os.path.isfile(tempfile):
            if filesize == os.path.getsize(tempfile):
                if 1:#filemd5 == FILEMD5:
                    print "file exists"
                    continue
            elif filesize > os.path.getsize(tempfile):
                print os.path.getsize(tempfile)
                status = int(math.floor(os.path.getsize(tempfile) / SEND_PACE))
                print status
        new_fileinfo.append([filename, filesize, status])
    return new_fileinfo


def trans_file(socket, filename, filesize, status):
    restsize = filesize
    #f = open_file(filename)
    with open(filename, 'a') as f:
        if not f:
            print "Open file failed"
            return openfailed
        if status != 0:
            print status * SEND_PACE
            restsize = restsize - status * SEND_PACE
            print restsize
            f.seek(status * SEND_PACE)
        buff = ""
        count = 0
        print 'file openning'
        print 'file handle position at %d' % f.tell()
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
        print 'file closed'
    return 1
