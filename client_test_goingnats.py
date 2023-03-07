import datetime as dt
import time
import threading
from goingnats import Client
from goingnats import one
from goingnats import request
from goingnats import publish


def publisher():
    """publish time.time() every second"""
    with Client(name="publisher") as client:
        while True:
            time.sleep(1)
            client.publish(subject=b"time.time", payload=f"{time.time()}".encode())

threading.Thread(target=publisher, daemon=True).start()

def responder():
    """respond to request for today with the date"""
    with Client(name="responder") as client:
        client.subscribe(subject=b"today")
        client.subscribe(subject=b"add")
        while True:
            for request in client.get():
                if request.subject == b"today":
                    # slow responder
                    time.sleep(2)
                    # will format the date according to payload or defaults to ...
                    format = request.payload.decode() if request.payload else "%Y-%m-%d"
                    response = f"{dt.date.today():{format}}".encode()
                elif request.subject == b"add":
                    response = _int_to_bytes(sum(json.loads(request.payload)))
                else:
                    continue
                client.publish(
                    subject=request.inbox,
                    payload=response,
                )

threading.Thread(target=responder, daemon=True).start()

# application
with Client(name="consumer") as client:
    print("--- one ---")
    print(one(subject=b"time.time"))
    print("--- client.subscribe + client.request ---")
    client.subscribe(subject=b"time.time")
    received = 0
    response = None
    while received < 5:
        # waits for at most 10 ms for messages
        for message in client.get(wait=10):
            print(message)
            received += 1
        if received == 3 and response is None:
            # publish
            publish(subject=b"time.time", payload=b"hijack")
            # request response are blocking
            response = client.request(subject=b"today", payload=b"%Y%m%d")
            print(response)
    print("--- request ---")
    print(request(subject=b"add", payload=b"[1, 2, 3]"))
    try:
        print(request(subject=b"today", wait=100))
    except TimeoutError as e:
        print(e)
# UserWarning: NOP - out of context manager
client.publish(subject=b"out.of.context.manager")
