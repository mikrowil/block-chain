import requests
import time
from backend.wallet.wallet import Wallet

BASE_ULR = 'http://localhost:5000/'


def get_blockchain():
    return requests.get(f'{BASE_ULR}/blockchain').json()


def get_blockchain_mine():
    return requests.get(f'{BASE_ULR}/blockchain/mine').json()


def post_wallet_transaction(recipient, amount):
    return requests.post(f'{BASE_ULR}/wallet/transact',
                         json={
                             'recipient': recipient,
                             'amount': amount
                         }).json()


def get_wallet_info():
    return requests.get(f'{BASE_ULR}/wallet/info').json()


start_blockchain = get_blockchain()
print(f'start chain: {start_blockchain}')

recipient = Wallet().address

post_wallet_trans_1 = post_wallet_transaction(recipient, 21)
print(f'\npost_wallet_trans_1: {post_wallet_trans_1}')

post_wallet_trans_2 = post_wallet_transaction(recipient, 13)
print(f'\npost_wallet_trans_2: {post_wallet_trans_2}')

time.sleep(1)
mined_block = get_blockchain_mine()
print(f'\nmined+block: {mined_block}')


wallet_info = get_wallet_info()
print(f'\nwallet info: {wallet_info}')
