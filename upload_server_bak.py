import os
import mimetypes
from flask import Flask, request, redirect, url_for, Response
from werkzeug import secure_filename
import random

import gevent
from gevent.threadpool import ThreadPool
from gevent import monkey
monkey.patch_all()

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tmpfile')
ALLOWED_EXTENSIONS = set(['png', 'mp4', 'swf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/download/<filename>', methods=['GET', 'POST'])
def asyn(filename):
    pool = ThreadPool(10)
    print "create pool"
    jobs = [pool.spawn(download_file, filename, (request))]
    gevent.wait(jobs)

#@app.route('/download/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    print filename
    if filename:
        mimeType, enc = mimetypes.guess_type(filename)
        data = open(os.path.join(UPLOAD_FOLDER, filename), 'rb').read()
        print "start download"
        if 'Range' in request.headers:
            start, end = request.headers['Range'][len('bytes='):].split('-')
            try:
                start = int(start)
            except ValueError:
                start = 0
            try:
                end = int(end)
            except ValueError:
                end = 0
            print "head over"
            response = Response(data[start:end], mimetype=mimeType)
            response.headers.add_header('Content-Range', 'bytes {0}-{1}/{2}'.format(start, end-1, len(data)))
            return response
        return Response(data, mimetype=mimeType)
    return '''
    <!doctype html>
    <title>Download File</title>
    <h1>Download File</h1>
    <form action="" method=get enctype=multipart/form-data>
        <input type=submit name="movie1.mp4" value="movie1.mp4">
        <input type=submit name="movie1.png" value="movie1.png">
    </form>

    '''


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files
        key = files.keys()[0]
        value = files[key]
        filename = value.filename
        print filename
        if files and allowed_file(filename):
            if 'Content-Range' in request.headers:
                range_str = request.headers['Content-Range']
                start_bytes = int(range_str.split(' ')[1].split('-')[0])
                with open(filename, 'a') as f:
                    f.seek(start_bytes)
                    f.write(value.stream.read())
            else:
                filename = secure_filename(filename)
                files['file'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload New File</title>
    <h1>Upload New File</h1>
    <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file></p>
        <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.debug = True
    app.run()
