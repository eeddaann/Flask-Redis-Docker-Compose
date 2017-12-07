__author__ = 'gadh'
from flask import Flask,render_template,request
import redis
# Make instance of Flask
app = Flask(__name__)
# Start Redis server
r=redis.StrictRedis('127.0.0.1',6379,0, decode_responses=True,charset='utf-8')


@app.route('/')
def start():
    return  render_template('index.html')

@app.route('/write',methods=['GET','POST'])
def write():
    if request.method=='GET':
        return render_template('write.html')
    elif request.method=='POST':
        key=request.form['key']
        val=request.form['val']
        r.set(key,val) #5
        return render_template('index.html')

@app.route('/read',methods=['GET','POST'])
def read():
    if request.method=='GET':
        return  render_template('read.html')
    elif request.method=='POST':
        key=request.form['key']
        val=r.get(key)
        return  render_template('read.html',val=val,key=key)

@app.route('/color',methods=['GET','POST'])
def color():
    brick = r.get('brickName') # get brick name from redis
    val = r.get(brick + ":color") # get current color
    return render_template('color.html', val=val) # send color to template and create webpage

@app.route('/drive',methods=['GET','POST'])
def drive():
    if request.method == 'GET':
        return render_template('drive.html')
    elif request.method == 'POST':
        brick = r.get('brickName')  # get brick name from redis
        color_db = r.get(brick + ":color") # get current color
        direction_db = r.get(brick + ":kivun") # get current direction
        requested_dir = request.form['do'] # get data from the form
        r.set(brick + ":kivun",requested_dir) # set the requested direction on redis
        return render_template('drive.html', color_db=color_db,direction_db=direction_db,requested_dir=requested_dir)

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')
