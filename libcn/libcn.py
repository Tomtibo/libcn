import base64
import json
import hashlib
import hmac
import configparser
import re
import os
import requests
#import socket
import urllib3
import time

class CypherNode:
    def __init__(self, \
        cnid=None, \
        key=None, \
        url=None, \
        configfile="{}/.cn/cn.conf".format(os.path.expanduser('~')), \
        unsecure=False, \
        verbose=False):
        """Cyphernode object reprensenting a cyphernode server"""
        self.stats_cmd = ['getblockchaininfo', 'getblockhash', 'helloworld', 'installation_info', 'getmempoolinfo']
        self.watcher_cmd = ['watch', 'unwatch', 'watchxpub', 'unwatchxpubbyxpub', 'unwatchxpubbylabel', 'getactivewatchesbyxpub',\
            'getactivewatchesbylabel', 'getactivexpubwatches', 'watchtxid', 'getactivewatches', 'get_txns_by_watchlabel',\
            'get_unused_addresses_by_watchlabel', 'getbestblockhash', 'getbestblockinfo', 'getblockinfo', 'gettransaction',\
            'ln_getinfo', 'ln_create_invoice', 'ln_getconnectionstring', 'ln_decodebolt11']
        self.spender_cmd = ['gettxnslist', 'getbalance', 'getbalances', 'getbalancebyxpub', 'getbalancebyxpublabel', 'getnewaddress',\
            'spend', 'bumpfee', 'addtobatch', 'batchspend', 'deriveindex', 'derivexpubpath', 'ln_pay', 'ln_newaddr', 'ots_stamp',\
            'ots_getfile', 'ln_getinvoice', 'ln_decodebolt11', 'ln_connectfund']
        #self.admin_cmd = ['conf', 'newblock', 'executecallbacks', 'ots_backoffice']
        self.all_cmd = []
        for itm in self.stats_cmd, self.watcher_cmd, self.spender_cmd: #, self.admin_cmd:
            for item in itm:
                self.all_cmd.append(item)
        self.unsecure = unsecure
        self.requests = requests
        self.h64 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9Cg=="
        if self.mode != 'client':
            if self.mode == 'server':
                self.cn_server_mode(self.port)
            elif self.mode == 'cypher':
                self.cn_cypher_mode()
        try:
            if cnid:
                self.cnid = cnid
            if key:
                self.key = key
            if url:
                self.url = url
            if configfile:  # If no explicit config provided, search for configfile in ~/.cn/cn.conf
                config = configparser.ConfigParser()
                config.read(configfile)
                for key in config.sections():
                    self.cnid = "{}".format(config.get(key, 'cnid')).replace('"', '')
                    self.key = "{}".format(config.get(key, 'key')).replace('"', '')
                    self.url = "{}".format(config.get(key, 'url')).replace('"', '')
        except ConnectionRefusedError:
            print('Authentification failed !')
            return None
        self.req = ['endpoint', 'headers=headers']
        if self.unsecure:
            urllib3.disable_warnings()
            self.req.append('verify=False')
        elif not self.unsecure:
            self.req.append('verify=True')
        if verbose:
            self.verbose()
    def inform(self, command):
        """Get info about specific command"""
        info_resp = None
        if command in self.all_cmd:
            if eval('self.{}'.format(command)):
                info_resp = eval('self.{}'.format(command)).__doc__
        return info_resp
    def listing(self, category):
        """Listing command"""
        for itm in eval('self.{}_cmd'.format(category)):
            print(itm)
        return
    def verbose(self):
        for key in dir(self):
            key_re = re.compile(r'__(.*)__')
            if not key_re.search(key):
                value = "self.{}".format(key)
                print("{} = {}".format(key, eval(value)))
    def get_token(self):
        token = None
        expire = round(time.time()) + 10
        p64 = {}
        p64['id'] = self.cnid
        p64['exp'] = expire
        bytes_p64 = json.dumps(p64).encode('utf-8')
        cv_p64 = base64.encodestring(bytes_p64)
        encoded_p64 = cv_p64.decode('utf-8').replace('\n', '')
        msg = '{}.{}'.format(self.h64, encoded_p64)
        sms = '{}'.format(hmac.new(key=self.key.encode('utf-8'), msg=msg.encode('utf-8'), digestmod=hashlib.sha256).hexdigest())
        token = "{}.{}.{}".format(self.h64, encoded_p64, sms)
        return token
    def get_headers(self):
        """Get autorisation headers"""
        headers = {"Authorization": "Bearer {}".format(self.get_token())}
        return headers
    # Handle requests
    def get_data(self, endpoint):
        """Get data request"""
        headers = self.get_headers()
        request = "self.requests.get{}.json()".format(tuple(self.req)).replace('\'', '')
        response = eval(request)
        return response
    def post_data(self, endpoint, payload):
        """Post data request"""
        headers = self.get_headers()
        self.req.append('data=payload')
        request = "self.requests.post{}.json()".format(tuple(self.req)).replace('\'', '')
        response = eval(request)
        return response
    # Experimental server modes
    def cn_server_mode(self, port):
        """Not working right now"""
        pass
    def cn_cypher_mode(self):
        """Not working right now"""
        pass
    # Get requests
    def getblockchaininfo(self):
        """Get blockchain information"""
        endpoint = "{}/getblockchaininfo".format(self.url)
        response = self.get_data(endpoint)
        return response
    def installation_info(self):
        """Get cyphernode installation information"""
        endpoint = "{}/installation_info".format(self.url)
        response = self.get_data(endpoint)
        return response
    def helloworld(self): ###############
        """Not working right now"""
        endpoint = "{}/helloworld".format(self.url)
        response = self.get_data(endpoint)
        return response
    def getmempoolinfo(self):
        """Ger memory pool information"""
        endpoint = "{}/getmempoolinfo".format(self.url)
        response = self.get_data(endpoint)
        return response
    def getbestblockhash(self):
        """Get best block hash"""
        endpoint = "{}/getbestblockhash".format(self.url)
        response = self.get_data(endpoint)
        return response
    def getbestblockinfo(self):
        """Get best block information"""
        endpoint = "{}/getbestblockinfo".format(self.url)
        response = self.get_data(endpoint)
        return response
    def ln_getinfo(self):
        """Get lightning information"""
        endpoint = "{}/ln_getinfo".format(self.url)
        response = self.get_data(endpoint)
        return response
    def ln_getconnectionstring(self):
        """Get lightning connection string"""
        endpoint = "{}/ln_getconnectionstring".format(self.url)
        response = self.get_data(endpoint)
        return response
    def ln_newaddr(self):
        """Get new lightning address"""
        endpoint = "{}/ln_newaddr".format(self.url)
        response = self.get_data(endpoint)
        return response
    def gettxnslist(self):################
        """Not working right now"""
        endpoint = "{}/gettxnslist".format(self.url)
        response = self.get_data(endpoint)
        return response
    def getbalance(self):
        """Get spender wallet balance"""
        endpoint = "{}/getbalance".format(self.url)
        response = self.get_data(endpoint)
        return response
    def getbalances(self):
        """Get spender wallet balance"""
        endpoint = "{}/getbalances".format(self.url)
        response = self.get_data(endpoint)
        return response
    def getactivewatches(self):
        """Get a list of watched address"""
        endpoint = "{}/getactivewatches".format(self.url)
        response = self.get_data(endpoint)
        return response
    def getactivexpubwatches(self):
        """Get a list of watched xpub"""
        endpoint = "{}/getactivexpubwatches".format(self.url)
        response = self.get_data(endpoint)
        return response
    # Get requests with optional argument
    def getnewaddress(self, *typeid):
        """Get new address"""
        if typeid:
            endpoint = "{}/getnewaddress/{}".format(self.url, typeid)
        else:
            endpoint = "{}/getnewaddress".format(self.url)
        response = self.get_data(endpoint)
        return response
    # Get request with argument(s)
    def getblockhash(self):
        "hashing"
        endpoint = "{}/getblockhash".format(self.url)
        response = self.get_data(endpoint)
        return response
    def unwatch(self, address):
        "address"
        endpoint = "{}/unwatch/{}".format(self.url, address)
        response = self.get_data(endpoint)
        return response
    def unwatchxpubbyxpub(self, xpub):
        "xpub"
        endpoint = "{}/unwatchxpubbyxpub/{}".format(self.url, xpub)
        response = self.get_data(endpoint)
        return response
    def unwatchxpubbylabel(self, label):
        "label"
        endpoint = "{}/unwatchxpubbylabel/{}".format(self.url, label)
        response = self.get_data(endpoint)
        return response
    def getactivewatchesbyxpub(self, xpub):
        "xpub"
        endpoint = "{}/getactivewatchesbyxpub/{}".format(self.url, xpub)
        response = self.get_data(endpoint)
        return response
    def getactivewatchesbylabel(self, label):
        "label"
        endpoint = "{}/getactivewatchesbylabel/{}".format(self.url, label)
        response = self.get_data(endpoint)
        return response
    def get_txns_by_watchlabel(self, label):
        "label"
        endpoint = "{}/get_txns_by_watchlabel/{}".format(self.url, label)
        response = self.get_data(endpoint)
        return response
    def get_unused_addresses_by_watchlabel(self, label):
        "label"
        endpoint = "{}/get_unused_addresses_by_watchlabel/{}".format(self.url, label)
        response = self.get_data(endpoint)
        return response
    def getblockinfo(self, block):
        "label"
        endpoint = "{}/getblockinfo/{}".format(self.url, block)
        response = self.get_data(endpoint)
        return response
    def gettransaction(self, txid):
        "txid"
        endpoint = "{}/gettransaction/{}".format(self.url, txid)
        response = self.get_data(endpoint)
        return response
    def ln_decodebolt11(self, bolt11):
        "label"
        endpoint = "{}/ln_decodebolt11/{}".format(self.url, bolt11)
        response = self.get_data(endpoint)
        return response
    def getbalancebyxpub(self, xpub):
        "label"
        endpoint = "{}/getbalancebyxpub/{}".format(self.url, xpub)
        response = self.get_data(endpoint)
        return response
    def getbalancebyxpublabel(self, label):
        "label"
        endpoint = "{}/getbalancebyxpublabel/{}".format(self.url, label)
        response = self.get_data(endpoint)
        return response
    def ots_getfile(self, hashing):
        "label"
        endpoint = "{}/ots_getfile/{}".format(self.url, hashing)
        response = self.get_data(endpoint)
        return response
    def ln_getinvoice(self, label):
        "label"
        endpoint = "{}/ln_getinvoice/{}".format(self.url, label)
        response = self.get_data(endpoint)
        return response
    # Post requests
    def watch(self, address, cburl0=None, cburl1=None, emsg=None):
        """address [unconfirmedCallbackURL confirmedCallbackURL eventMessage]"""
        endpoint = "{}/watch".format(self.url)
        payload = {"address":address, "unconfirmedCallbackURL":cburl0, "confirmedCallbackURL":cburl1, "eventMessage":emsg}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def watchxpub(self, xpub, label=None, path="0/n", nstart=0, cburl0=None, cburl1=None): # "0/1/n" electrum = 0/n(receiving) 1/n(change)
        """xpub [label path nstart unconfirmedCallbackURL confirmedCallbackURL]"""
        endpoint = "{}/watchxpub".format(self.url)
        payload = {"label":label, "pub32":xpub, "path":path, "nstart":int(nstart), "unconfirmedCallbackURL":cburl0, "confirmedCallbackURL":cburl1}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def watchtxid(self, txid, cburl1=None, xcburl=None, xconf=6):############
        "txid [cburl xcburl xconf]"
        endpoint = "{}/watchtxid".format(self.url)
        payload = {"txid":txid, "confirmedCallbackURL":cburl1, "xconfCallbackURL":xcburl, "nbxconf":int(xconf)}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def spend(self, address, amount, emsg=None):
        """address amount [eventMessage]"""
        endpoint = "{}/spend".format(self.url)
        payload = {"address":address, "amount":amount, "eventMessage":emsg}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def bumpfee(self, txid, conf_target):
        """txid confTarget"""
        endpoint = "{}/bumpfee".format(self.url)
        payload = {"txid":txid, "confTarget":conf_target}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def addtobatch(self, address, amount):
        """address amount"""
        endpoint = "{}/addtobatch".format(self.url)
        payload = {"address":address, "amount":amount}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def derivexpubpath(self, xpub, path):
        """xpub path"""
        endpoint = "{}/derivexpubpath".format(self.url)
        payload = {"xpub":xpub, "path":path}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def ln_create_invoice(self, msatoshi, label=None, description=None, cburl=None, expiry=900):
        """msatoshi [label description callbackUrl expiry]"""
        endpoint = "{}/ln_create_invoice".format(self.url)
        payload = {"msatoshi":msatoshi, "label":label, "description":description, "expiry":expiry, "callbackUrl":cburl}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def ln_pay(self, bolt11, expected_msatoshi, expected_description):
        """bolt11 expected_msatoshi expected_description"""
        endpoint = "{}/ln_pay".format(self.url)
        payload = {"bolt11":bolt11, "expected_msatoshi":expected_msatoshi, "expected_description":expected_description}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def ln_connectfund(self, url, msatoshi, cburl=None):
        """peer msatoshi [callbackUrl]"""
        endpoint = "{}/ln_connectfund".format(self.url)
        payload = {"peer":url, "msatoshi":msatoshi, "callbackUrl":cburl}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def ots_stamp(self, hashing, cburl=None):
        """hash [callbackUrl]"""
        endpoint = "{}/ots_stamp".format(self.url)
        payload = {"hash":hashing, "callbackUrl":cburl}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def ots_verify(self, hashing, otsfile):
        """hash base64otsfile"""
        endpoint = "{}/ots_verify".format(self.url)
        payload = {"hash":hashing, "base64otsfile":otsfile}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
    def ots_info(self, hashing=None, otsfile=None):
        """[hash base64otsfile]"""
        endpoint = "{}/ots_info".format(self.url)
        payload = {"hash":hashing, "base64otsfile":otsfile}
        payload = json.dumps(payload)
        response = self.post_data(endpoint, payload)
        return response
"""     # Callbacks requests
    def conf(self):##########
        Not working right now"
        endpoint = "{}/conf".format(self.url)
        response = self.get_data(endpoint)
        return response
    def newblock(self):##########
        Not working right now"
        endpoint = "{}/newblock".format(self.url)
        response = self.get_data(endpoint)
        return response
    def executecallbacks(self):###########
        "Not working right now"
        endpoint = "{}/executecallbacks".format(self.url)
        response = self.get_data(endpoint)
        return response
    def ots_backoffice(self):#########
        Not working right now"
        endpoint = "{}/ots_backoffice".format(self.url)
        response = self.get_data(endpoint)
        return response
<<<<<<< master
=======

 """
class CallbackServer:
    """CallbackServer is a socket server used in a child class to
    listen incoming callbacks request"""
    def __init__(self, port):
        """Initialyse callback server"""
        self.port = port
    def accept_wrapper(self, sock):
        """Accept incoming connections"""
        conn, addr = sock.accept()
        #print("accepted connection from", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
    def get_headers(self, response_code, lenght):
        """Build response headers"""
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'
        header += 'Content-Length: {}\n\n'.format(lenght)
        return header
    def service_connection(self, key, mask):
        """Execute actions on incomming callbacks"""
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += recv_data
            else:
            #   print("closing connection to", data.addr)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                request = None
                callback = None
                #print('Data = {}'.format(data.outb))
                requestRe = re.compile(b'POST\ \/(.*)\ ')
                if requestRe.search(data.outb):
                    request = requestRe.search(data.outb).group(1)
                    request = request.decode('utf-8')
                    #print('request = {}'.format(request))
                jsonRe = re.compile(b'{(.*)}')
                if jsonRe.search(data.outb):
                    callback = jsonRe.search(data.outb).group(1)
                    callback = callback.decode('utf-8')
                    callback = '{}{}{}'.format("{", callback, "}")
                    callback = json.loads(callback)
                    callback = json.dumps(callback)
                    #print(callback)
                if request and callback:
                        try:
                            response = eval('self.{}({})'.format(request, callback))
                            if not response:
                                response = 'True'
                            leng = len(response)
                            headers = self.get_headers(200, leng)
                            sent = sock.send(bytes('{}{}'.format(headers, response).encode('utf-8')))
                            data.outb = data.outb[sent:]
                        except ChildProcessError:
                            response = 'False'
                            leng = len(response)
                            headers = self.get_headers(404, leng)
                            sent = sock.send(bytes('{}{}'.format(headers, response).encode('utf-8')))
                            data.outb = data.outb[sent:]
    def start(self):
        """CallbacksServer main process to start listen"""
        host = ''
        port = int(self.port)
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        #print("listening on", (host, port))
        lsock.setblocking(False)
        self.sel = selectors.DefaultSelector()
        self.sel.register(lsock, selectors.EVENT_READ, data=None)
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    #print('{} = {}'.format(key, mask))
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except Warning:
            print("CallbackServer Warning")
        finally:
            self.sel.close()
>>>>>>> local
