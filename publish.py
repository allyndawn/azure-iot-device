# Azure IoT Publish Example
#
# Allen Snook
# January 30, 2021

import os
import asyncio
import uuid
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import time
import random
import json

async def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    await device_client.connect()
    print("Connected!")

    # Send a message every 15 seconds
    try:
        while True:
            roll = random.randint(1,20)
            print("Rolled a", roll)
            payload={"value": roll}
            msg = Message(json.dumps(payload))
            msg.message_id = uuid.uuid4()
            msg.correlation_id = "correlation-1234"
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"
            await device_client.send_message(msg)
            print("Press Ctrl-C to stop")
            time.sleep(15)
    except KeyboardInterrupt:
        pass

    # Finally, shut down the client
    await device_client.shutdown()
    print("Disonnected!")

if __name__ == "__main__":
    asyncio.run(main())
