import uuid
from backend.config import STARTING_BALANCE


class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of the miners balance.
    Allows auth on transactions
    """

    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
