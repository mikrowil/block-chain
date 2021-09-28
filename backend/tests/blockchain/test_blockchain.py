import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA


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
        blockchain.addBlock(i)
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
