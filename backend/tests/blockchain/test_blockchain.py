import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.addBlock(data)

    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_ten_blocks():
    blockchain = Blockchain()
    for i in range(10):
        blockchain.addBlock([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain


def test_is_valid_chain(blockchain_ten_blocks):
    Blockchain.is_valid_chain(blockchain_ten_blocks.chain)


def test_is_valid_chain_bad_genesis(blockchain_ten_blocks):
    blockchain_ten_blocks.chain[0].hash = 'bad_hash_browns'

    with pytest.raises(Exception, match='Genesis must be valid'):
        Blockchain.is_valid_chain(blockchain_ten_blocks.chain)


def test_replace_chain(blockchain_ten_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_ten_blocks.chain)

    assert blockchain.chain == blockchain_ten_blocks.chain


def test_replace_chain_shorter(blockchain_ten_blocks):
    blockchain = Blockchain()

    with pytest.raises(Exception, match='Cannot replace. The incoming chain must be longer'):
        blockchain_ten_blocks.replace_chain(blockchain.chain)


def test_replace_chain_invalid_chain(blockchain_ten_blocks):
    blockchain = Blockchain()
    blockchain_ten_blocks.chain[3].hash = 'bad_hash_browns'

    with pytest.raises(Exception, match='The incoming chain is invalid'):
        blockchain.replace_chain(blockchain_ten_blocks.chain)


def test_valid_transaction_chain(blockchain_ten_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)


def test_is_valid_transaction_chain_duplicate_transactions(blockchain_ten_blocks):
    transaction = Transaction(Wallet(), 'recipient', 1).to_json()

    blockchain_ten_blocks.addBlock([transaction, transaction])

    with pytest.raises(Exception, match="is not unique"):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)


def test_is_valid_transaction_chain_multiple_rewards(blockchain_ten_blocks):
    reward_1 = Transaction.reward_transaction(Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(Wallet()).to_json()

    blockchain_ten_blocks.addBlock([reward_1, reward_2])

    with pytest.raises(Exception, match="one mining reward per block"):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)


def test_is_valid_transaction_chain_bad_transaction(blockchain_ten_blocks):
    bad_transaction = Transaction(Wallet(), 'recipient', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)

    blockchain_ten_blocks.addBlock([bad_transaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)


def test_is_valid_transaction_chain_bad_historic_balance(blockchain_ten_blocks):
    wallet = Wallet()
    bad_trans = Transaction(wallet, 'recipient', 1)
    bad_trans.output[wallet.address] = 9000
    bad_trans.input['amount'] = 9001
    bad_trans.input['signature'] = wallet.sign(bad_trans.output)

    blockchain_ten_blocks.addBlock([bad_trans.to_json()])

    with pytest.raises(Exception, match='has an invalid input amount'):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)

