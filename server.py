import pickle

class RPCHandler():

    def __init__(self):
        self._functions = {}

    def register_functions(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        """Method that handles RPC request. Note that the connection socket is passed down as an argument

        Parameters
        ----------
        connection: socket object
            client socket

        """

        try:
            while True:

                # the function name and arguments are extracted

                func_name, args, kwargs = pickle.loads(connection.recv())

                # the function is then run and the values are returned via the connection

                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(r))

                except Exception as err:
                    print(err)

        except EOFError:
            pass

# the above needs to be used with some form of messaging server. The multiprocessing module provides a simple option

from multiprocessing.connection import Listener, Client
from threading import Thread

def rpc_server(handler, address, authkey):

    sock = Listener(address, authkey=authkey)

    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client, ))
        t.daemon = True
        t.start()


def add(x,y):
    return x + y

def sub(x, y):
    return x - y

# the functions are then registered

handler = RPCHandler()
handler.register(add)
handler.register(sub)

# the server is then run

rcp_server(handler, ('localhost', 17000), authkey=b'peekaboo')
