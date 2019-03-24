class RPCProxy():

    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):

        def do_rpc(*args, **kwargs):
            self._connection.send(pickel.dumps((names, args, kwargs)))
            results = pickle.loads(self._connection.revc())

            if istinstance(result, Exception):
                raise result
            return result
        return do_rpc

# the proxy is essentially a wrapper for a client

c = Client(('localhost', 17000), authkey=b'peekaboo')
proxy = RPCProxy(c)

# functions registered on the Server can then be called

a = proxy.add(2,4)
b = proxy.sub(11,5)
