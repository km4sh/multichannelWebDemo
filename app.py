from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sys

app =  Flask(__name__)

@app.route('/',  methods=['POST',  'GET'])
def  index():
    return render_template('index.html')

@app.route('/records',  methods=['POST',  'GET'])
def  record():
    if request.method ==  'POST':
        audio = request.form
        print(sys.getsizeof(audio['upfile_b64']))
        return  'OK'
    else:
        app.logger.info("好紧张有人点开了这个页面！")
        return  render_template('records.html')

if  __name__  ==  "__main__":
    app.run(debug=True)