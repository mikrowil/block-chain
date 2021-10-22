import time

from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.util.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.data = data
        self.last_hash = last_hash
        self.timestamp = timestamp
        self.hash = hash
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return ('Block('
                f'timestamp: {self.timestamp},'
                f'last_hash: {self.last_hash},'
                f'hash: {self.hash},'
                f'data: {self.data},'
                f'difficulty: {self.difficulty},'
                f'nonce {self.nonce}'
                )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """Serialize the block"""
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def generate_genesis():
        # return Block(GENESIS_DATA['timestamp'],
        #              GENESIS_DATA['last_hash'],
        #              GENESIS_DATA['hash'],
        #              GENESIS_DATA['data'])
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json):
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the difficulty according to the MINE_RATE
        :param last_block:
        :param new_timestamp:
        :return: adjusted difficulty
        """

        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid(last_block, block):
        """
        checks if block is valid
        :param last_block:
        :param block:
        :return:
        """
        if block.last_hash != last_block.hash:
            raise Exception('The last_hash must be the same')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('Proof of work requirement not met')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('Difficulty can only adjust by one')

        re_hash = crypto_hash(
            block.timestamp, block.last_hash, block.data, block.difficulty, block.nonce
        )
        if block.hash != re_hash:
            raise Exception('Hash value not consistent')


def main():
    gen_block = Block.generate_genesis()
    bad_block = Block.mine_block(gen_block, 'foo')
    bad_block.last_hash = 'evil data'

    try:
        Block.is_valid(gen_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')


if __name__ == '__main__':
    main()
