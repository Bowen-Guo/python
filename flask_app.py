"""This server can only handle one request a time"""

from flask import Flask
from time import sleep

app = Flask(__name__)

@app.route('/helloworld', methods=['GET'])
def hello_world():
    print('Receive request')
    sleep(10)
    return 'Hello world!'

if __name__ == '__main__':
    app.run(threaded=True)
