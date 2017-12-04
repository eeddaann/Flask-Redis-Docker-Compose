__author__ = 'gadh'
from flask import Flask,render_template,request
import redis
# Make instance of Flask
app = Flask(__name__)
# Start Redis server
r=redis.StrictRedis('redis',6379,1, decode_responses=True,charset='utf-8')


@app.route('/')
def start():
    return  render_template('hadgama.html')

@app.route('/write',methods=['GET','POST']) #1
def write():
    if request.method=='GET':
        return render_template('write.html') #2
    elif request.method=='POST': #3
        key=request.form['key'] #4
        val=request.form['val']
        r.set(key,val) #5
        return render_template('index.html') #6

@app.route('/read',methods=['GET','POST'])
def read():
    if request.method=='GET':
        return  render_template('read.html') #1
    elif request.method=='POST': #2
        key=request.form['key'] #3
        val=r.get(key) #4
        return  render_template('read.html',val=val,key=key) #5


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0') #6
