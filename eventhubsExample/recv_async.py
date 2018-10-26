#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show running concurrent receivers.
"""
import datetime
import os
import sys
import time
import logging
import asyncio
from azure.eventhub import Offset, EventHubClientAsync, AsyncReceiver

# import examples
# logger = examples.get_logger(logging.INFO)

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
ADDRESS = "amqps://Home-eventhubs.servicebus.windows.net/eventhubs-web"

# SAS policy and key are not required if they are encoded in the URL
# USER = os.environ.get('EVENT_HUB_SAS_POLICY')
# KEY = os.environ.get('EVENT_HUB_SAS_KEY')
USER = "yytangKey"
KEY = "nGor+O62XsKK2/AjJp+q4poO5pAlHBzyDVRi9FdLU9I="
CONSUMER_GROUP = "$default"
# OFFSET = Offset(datetime.datetime.utcnow())"
OFFSET = Offset("-1")


async def pump(client, partition):
    receiver = client.add_async_receiver(CONSUMER_GROUP, partition, OFFSET, prefetch=5)
    await client.run_async()
    total = 0
    start_time = time.time()
    for event_data in await receiver.receive():
        last_offset = event_data.offset
        last_sn = event_data.sequence_number
        msg = event_data.body_as_str()
        print("Received: {}, {}, {}".format(last_offset.value, last_sn, msg))
        total += 1
    end_time = time.time()
    run_time = end_time - start_time
    print("Received {} messages in {} seconds".format(total, run_time))

try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")

    loop = asyncio.get_event_loop()
    client = EventHubClientAsync(ADDRESS, debug=False, username=USER, password=KEY)
    tasks = [
        asyncio.ensure_future(pump(client, "0")),
        asyncio.ensure_future(pump(client, "1"))
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_until_complete(client.stop_async())
    loop.close()

except KeyboardInterrupt:
    pass