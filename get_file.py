import httplib2
import os

url = 'http://127.0.0.1:5000/download/VTS_02_1.swf'
DOWNLOAD_FOLDER = '/Users/achivil/tmpfile/'

def download(filename, end_length):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    count = 0
    pace = 4096
    h = httplib2.Http()
    while count < end_length:
        start = count
        count += pace
        end = count - 1
        byte = 'bytes=%d-%d' % (start, end)
        headers = {'Range': byte}
        response, content = h.request(url, headers=headers)
        #print content
        pos = count
        with open(path, 'wb+') as f:
            f.seek(start)
            #print start
            f.write(content)
            f.close()

if __name__ == "__main__":
    download('VTS_02_1.swf', 81280843)
