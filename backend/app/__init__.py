import os
import requests
import random

from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)


@app.route('/')
def route_default():
    return 'Welcome crypto maniacs'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_mine_block():
    trans_data = 'Some_data_here'
    blockchain.addBlock(trans_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())


ROOT_PORT = 5000
PORT = 5000

if os.environ.get('PEER'):
    PORT = random.randint(5001, 6000)

    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'result.json(): {result.json()}')

    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain)
    except Exception as e:
        print(f'\n --Could not replace chain. msg:{e}')

app.run(port=PORT)
