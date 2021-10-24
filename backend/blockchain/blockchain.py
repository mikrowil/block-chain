from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT


class Blockchain:
    def __init__(self):
        self.chain = [Block.generate_genesis()]

    def addBlock(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace local chain with incoming chain if the following rules apply
            - Incoming chain is longer than the local one
            - The incoming chain is formatted correctly
        :param chain:
        :return:
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        """Serialize the blockchain to be converted to json"""
        return list(map(lambda x: x.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """Deserialize a list of blocks into a blockchain instance"""
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )

        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validates a chain
            - Must start with a genesis block
            - blocks must be formatted correctly
        :param chain:
        :return:
        """
        if chain[0] != Block.generate_genesis():
            raise Exception('Genesis must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        transaction_ids = set()

        for index in range(len(chain)):
            block = chain[index]
            has_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')
                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_reward:
                        raise Exception(
                            'There can only be one mining reward per block. '
                            f'Check block with hash: {block.hash}'
                        )
                    has_reward = True
                else:

                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:index]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid input amount')

                Transaction.is_valid(transaction)


def main():
    blockchain = Blockchain()
    blockchain.addBlock('1')
    blockchain.addBlock('2')
    blockchain.addBlock('3')

    print(blockchain)


if __name__ == '__main__':
    main()
