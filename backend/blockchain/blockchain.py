from backend.blockchain.block import Block


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


def main():
    blockchain = Blockchain()
    blockchain.addBlock('1')
    blockchain.addBlock('2')
    blockchain.addBlock('3')

    print(blockchain)


if __name__ == '__main__':
    main()
