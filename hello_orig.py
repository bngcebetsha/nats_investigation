import asyncio
import nats

async def main():
    # Connect to NATS!
    #nc = await nats.connect("demo.nats.io")
    nc = await nats.connect()

    # Receive messages on 'foo'
    sub = await nc.subscribe("*", message_handler())

    # Publish a message to 'foo'
    await nc.publish("foo", b'Hello from Python!')

    # Process a message
    msg = await sub.next_msg()
    print("Received:", msg)

    # Close NATS connection
    await nc.close()


def message_handler():
    pass

if __name__ == '__main__':
    #asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
