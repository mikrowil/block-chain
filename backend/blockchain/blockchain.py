from backend.blockchain.block import Block


class Blockchain:
    def __init__(self):
        self.chain = [Block.generate_genesis()]

    def addBlock(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'


def main():
    blockchain = Blockchain()
    blockchain.addBlock('1')
    blockchain.addBlock('2')
    blockchain.addBlock('3')

    print(blockchain)


if __name__ == '__main__':
    main()
