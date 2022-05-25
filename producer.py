#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json

from pprint import pprint as pp
from websocket import WebSocketApp
import websocket

URL = "wss://testnet-explorer.binance.org/ws/block"
kinesis = boto3.client('kinesis')


def on_message(_, msg):
    json_msg = json.loads(msg)
    if 'blockHash' in json_msg:
        print('Publishing...')
        response = kinesis.put_record(
                StreamName='brianz-gdax-dev-kinesis-stream',
                PartitionKey=json_msg['blockHash'],
                Data=msg + '|||',
        )
        pp(response)
    else:
        pp(json_msg)


def on_open(socket):
    """Callback executed at socket opening.

    Keyword argument:
    socket -- The websocket itself
    """

    products = ["blockHeight", "blockNode"]
    channels = [
        {
            "name": "ticker",
            "product_ids": products,
        },
    ]

    params = {
        "type": "subscribe",
        "channels": channels,
    }
    socket.send(json.dumps(params))


def main():
    """Main function."""
    websocket.enableTrace(True)
    ws = WebSocketApp(URL, on_open=on_open, on_message=on_message)
    ws.run_forever()


if __name__ == '__main__':
    main()
