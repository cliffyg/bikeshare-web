import socket
import json

# Class which acts as an interface to S-Store.
class SstoreClient(object):
    addr = None
    port = None
    s = None
    buf = None
    connected = False
    
    def __init__(self, addr='localhost', port=6000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.port = port
        self.buf = b''
        self.connected = False

    def connect(self):
        if not self.connected:
            self.s.connect((self.addr, self.port))
            self.connected = True
        return self.connected

    def disconnect(self):
        if self.connected:
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.s = None
            self.connected = False
        return

    def call_proc(self, proc='', args='', keepalive=False):
        msg = ''
        try:
            # Connect first, if necessary.
            if not self.connected:
                self.connect()
            # Clear buffer.
            self.buf = b''
            # Construct the object which will be converted to JSON and sent to the
            # database client.
            call = dict()
            call['proc'] = proc
            call['args'] = list()
            for arg in args:
                call['args'] += [arg]
            # Send JSON to the database client, then receive results.
            self.s.sendall(json.dumps(call, ensure_ascii=True) + "\r\n")
            data = self.s.recv(1024)
            while data:
                self.buf += data
                data = self.s.recv(1024)
            rtn = json.loads(self.buf)
        except Exception as e:
            rtn = json.loads('{"data":[],"success":0}')
            msg = str(e)
        finally:
            rtn['msg'] = msg
        # If we haven't instructed the connection to stay open, disconnect.
        if not keepalive:
            self.disconnect()
        return rtn
