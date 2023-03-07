## Starting up NATS server and connecting to it for publishing/subscribing messages

#### Server
CAM dev boxes already have an instance of nats running from `/usr/bin/gnatsd` with config
found in `/etc/gnatsd.conf`.

#### Client
Various client apps can be downloaded from https://nats.io/download/ and for this example
we use this client https://github.com/3kwa/goingnats to connect to our local NATS server
to do basic publication and subscription for messages.

###### Running the script
```python
python3 client_test_goingnats.py
```
The current output looks like:
```shell
Traceback (most recent call last):
  File "client_test_goingnats.py", line 4, in <module>
    from goingnats import Client
  File "/home/kat/.local/lib/python3.6/site-packages/goingnats.py", line 43, in <module>
    class Client:
  File "/home/kat/.local/lib/python3.6/site-packages/goingnats.py", line 57, in Client
    def get(self, *, wait: Optional[int] = None) -> list[Union[Message, Request]]:
TypeError: 'type' object is not subscriptable
```

