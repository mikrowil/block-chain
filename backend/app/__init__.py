from flask import Flask
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()


@app.route('/')
def route_default():
    return 'Welcome crypto maniacs'


@app.route('/blockchain')
def route_blockchain():
    return blockchain.__repr__()


if __name__ == '__main__':
    app.run()
