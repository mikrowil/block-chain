import os
import time
from abc import ABC

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

publish_key = os.environ['PUB_KEY']
subscribe_key = os.environ['SUB_KEY']

pnc_config = PNConfiguration()
pnc_config.publish_key = publish_key
pnc_config.subscribe_key = subscribe_key

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}


class Listener(SubscribeCallback, ABC):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pub, message_object):
        print(f'\n-- CHANNEL -- {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            maybe_chain = self.blockchain.chain[:]
            maybe_chain.append(block)

            try:
                self.blockchain.replace_chain(maybe_chain)
                print(f'\n Replaced chain wonderfully')
            except Exception as e:
                print(f'\n Did not replace chain. Message: {e}')


class PubSub():
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnc_config)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        self.publish(CHANNELS['BLOCK'], block.to_json())


def main():
    pubsub = PubSub(Blockchain())

    time.sleep(1)

    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
    main()
