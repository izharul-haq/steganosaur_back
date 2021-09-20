import sys
import logging
from flask import Flask
from flask_cors import CORS

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def default():
    return 'OK'


if __name__ == '__main__':
    app.run()
