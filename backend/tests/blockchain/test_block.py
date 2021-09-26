from backend.blockchain.block import Block, GENESIS_DATA


def test_mine_block():
    last_block = Block.generate_genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash


def test_genesis():
    genesis = Block.generate_genesis()

    assert isinstance(genesis, Block)

    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value
