from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_clear_blockchain_transactions():
    pool = TransactionPool()
    trans_1 = Transaction(Wallet(), 'recipient', 1)
    trans_2 = Transaction(Wallet(), 'recipient', 2)

    pool.set_transaction(trans_1)
    pool.set_transaction(trans_2)
    blockchain = Blockchain()
    blockchain.addBlock([trans_1.to_json(), trans_2.to_json()])

    assert trans_1.id in pool.transaction_map
    assert trans_2.id in pool.transaction_map

    pool.clear_blockchain_transactions(blockchain)

    assert trans_1.id not in pool.transaction_map
    assert trans_2.id not in pool.transaction_map

