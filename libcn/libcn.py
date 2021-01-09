"""libcn is a client and server library for cyphernode"""
import base64
import json
import hashlib
import hmac
import configparser
import re
import os
import selectors
import types
import time
import socket
import requests
import urllib3
class CypherNode:
    """CypherNode class is a cyphernode client library"""
    def __init__(self, \
        cnid=None, \
        key=None, \
        url=None, \
        cert=None, \
        configfile="{}/.cn/cn.conf".format(os.path.expanduser('~')), \
        unsecure=False, \
        verbose=False):
        """Cyphernode object reprensenting a cyphernode server"""
        stats_cmd = ['getblockchaininfo', 'getblockhash', \
            'helloworld', 'installation_info', 'getmempoolinfo']
        watcher_cmd = ['watch', 'unwatch', 'watchxpub', \
            'unwatchxpubbyxpub', 'unwatchxpubbylabel', 'getactivewatchesbyxpub',\
            'getactivewatchesbylabel', 'getactivexpubwatches', \
                'watchtxid', 'getactivewatches', 'get_txns_by_watchlabel',\
            'get_unused_addresses_by_watchlabel', 'getbestblockhash', \
                'getbestblockinfo', 'getblockinfo', 'gettransaction',\
            'ln_getinfo', 'ln_create_invoice', 'ln_getconnectionstring', \
                'ln_decodebolt11', 'ln_listpeers', 'ln_getroute', 'ln_listpays']
        spender_cmd = ['getbalance', 'getbalances', \
            'getbalancebyxpub', 'getbalancebyxpublabel', 'getnewaddress',\
            'spend', 'bumpfee', 'addtobatch', 'batchspend', 'deriveindex', \
                'derivepubpath', 'ln_pay', 'ln_newaddr', 'ots_stamp', 'ots_info', 'ots_verify',\
            'ots_getfile', 'ln_getinvoice', 'ln_decodebolt11', 'ln_connectfund', \
            'ln_delinvoice', 'ln_listfunds', 'ln_withdraw', 'get_txns_spending']
        admin_cmd = ['conf', 'newblock', 'executecallbacks', 'ots_backoffice']
        self.all_cmd = []
        for itm in stats_cmd, watcher_cmd, spender_cmd: #, admin_cmd:
            for item in itm:
                self.all_cmd.append(item)
        self.requests = requests
        self.h64 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9Cg=="
        self.cnid = cnid
        self.key = key
        self.url = url
        self.cert = cert
        try:
            if configfile:  # If no explicit config provided, search for configfile in ~/.cn/cn.conf
                config = configparser.ConfigParser()
                config.read(configfile)
                for k in config.sections():
                    self.cnid = "{}".format(config.get(k, 'cnid')).replace('"', '')
                    self.key = "{}".format(config.get(k, 'key')).replace('"', '')
                    self.url = "{}".format(config.get(k, 'url')).replace('"', '')
                    self.cert = "{}".format(config.get(k, 'cert')).replace('"', '')
            self.auth = []
            if self.cnid == '003':
                for itm in stats_cmd, watcher_cmd, spender_cmd, admin_cmd:
                    for item in itm:
                        self.auth.append(item)
            elif self.cnid == '002':
                for itm in stats_cmd, watcher_cmd, spender_cmd:
                    for item in itm:
                        self.auth.append(item)
            elif self.cnid == '001':
                for itm in stats_cmd, watcher_cmd:
                    for item in itm:
                        self.auth.append(item)
            elif self.cnid == '000':
                for itm in stats_cmd:
                    self.auth.append(itm)
        except ConnectionError:
            print('Authentification failed !')
            return None
        self.req = ['endpoint', 'headers=headers']
        if unsecure:
            urllib3.disable_warnings()
            self.req.append('verify=False')
        elif self.cert:
                self.req.append('verify="{}"'.format(self.cert))
        else:
            print('Error! Invalid ssl certificate, use --cert with a valid cert, or bypass cert validation with the -u, --unsecure option')
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
        if eval('self.{}_cmd'.format(category)):
            for itm in eval('self.{}_cmd'.format(category)):
                print(itm)
    def verbose(self):
        """Verbose mode"""
        for key in dir(self):
            key_re = re.compile(r'__(.*)__')
            if not key_re.search(key):
                value = "self.{}".format(key)
                print("{} = {}".format(key, eval(value)))
    def get_token(self):
        """Token encoding"""
        token = None
        expire = round(time.time()) + 10
        p64 = {}
        p64['id'] = self.cnid
        p64['exp'] = expire
        bytes_p64 = json.dumps(p64).encode('utf-8')
        cv_p64 = base64.encodestring(bytes_p64)
        encoded_p64 = cv_p64.decode('utf-8').replace('\n', '')
        msg = '{}.{}'.format(self.h64, encoded_p64)
        sms = '{}'.format(hmac.new(key=self.key.encode('utf-8'), \
            msg=msg.encode('utf-8'), digestmod=hashlib.sha256).hexdigest())
        token = "{}.{}.{}".format(self.h64, encoded_p64, sms)
        return token
    def get_headers(self):
        """Get autorisation headers"""
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer {}".format(self.get_token())
        headers["Connection"] = "close"
        return headers
    def get_data(self, call, endpoint):
        """Get data request"""
        if call in self.auth:
            headers = self.get_headers()
            if headers and endpoint:
                request = "self.requests.get{}.json()".format(tuple(self.req)).replace('\'', '')
                #print(request)
                response = eval(request)
                return response
            else:
                return None
        else:
            raise ConnectionError
    def post_data(self, call, endpoint, payload):
        """Post data request"""
        if call in self.auth:
            headers = self.get_headers()
            if headers and endpoint and payload:
                self.req.append('data=payload')
                request = "self.requests.post{}.json()".format(tuple(self.req)).replace('\'', '')
                #print(request)
                response = eval(request)
                return response
            else:
                return None
        else:
            raise ConnectionError
    def getblockchaininfo(self):
        """Get blockchain informations"""
        call = 'getblockchaininfo'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def installation_info(self):
        """Get cyphernode installation informations"""
        call = 'installation_info'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def helloworld(self): ###############
        """Helloword exemple, returning error because is not json format"""
        call = 'helloworld'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def getmempoolinfo(self):
        """Get memory pool informations"""
        call = 'getmempoolinfo'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def getbestblockhash(self):
        """Get the hash of the best block"""
        call = 'getbestblockhash'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def getbestblockinfo(self):
        """Get best block informations"""
        call = 'getbestblockinfo'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def ln_getinfo(self):
        """Get lightning node informations"""
        call = 'ln_getinfo'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def ln_getconnectionstring(self):
        """Get lightning connection string"""
        call = 'ln_getconnectionstring'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def ln_newaddr(self):
        """Get new lightning deposit address"""
        call = 'ln_newaddr'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def ln_listpeers(self):
        """Get a list of lightning peers/channels"""
        call = 'ln_listpeers'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def ln_listfunds(self):
        """Get a list of lightning wallet funds"""
        call = 'ln_listfunds'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def ln_listpays(self):
        """Get a list of payed invoices"""
        call = 'ln_listpays'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def getbalance(self):
        """Get bitcoin spender wallet balance"""
        call = 'getbalance'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def getbalances(self):
        """Get bitcoin spender wallet balance with unconfirmed transactions"""
        call = 'getbalances'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def getactivewatches(self):
        """Get a list of watched address"""
        call = 'getactivewatches'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def getactivexpubwatches(self):
        """Get a list of watched xpub"""
        call = 'getactivexpubwatches'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def get_txns_spending(self):
        """Get transactions not spend from bitcoin spending wallet"""
        call = 'get_txns_spending'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def batchspend(self):
        """Spend bached transactions with addtobatch"""
        call = 'batchspend'
        endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    # Get requests with optional argument
    def getnewaddress(self, *typeid):
        """Get new spending bitcoin address
[(bech32,legacy,p2sh-segwit)]"""
        call = 'getnewaddress'
        if typeid:
            endpoint = "{}/{}/{}".format(self.url, call, typeid)
        else:
            endpoint = "{}/{}".format(self.url, call)
        response = self.get_data(call, endpoint)
        return response
    def ln_getroute(self, nodeid, msatoshi, *risk):
        """Get lighning node route
nodeid msatoshi [risk]""" 
        call = 'ln_getroute'
        if risk:
            endpoint = "{}/{}/{}/{}/{}".format(self.url, call, nodeid, msatoshi, risk)
        else:
            endpoint = "{}/{}/{}/{}".format(self.url, call, nodeid, msatoshi)
        response = self.get_data(call, endpoint)
        return response
    def get_txns_by_watchlabel(self, label, *count):
        """Get transaction not spend by watch label
label [count]"""
        call = 'get_txns_by_watchlabel'
        if count:
            endpoint = "{}/{}/{}/{}".format(self.url, call, label, count)
        else:
            endpoint = "{}/{}/{}".format(self.url, call, label)
        response = self.get_data(call, endpoint)
        return response
    def get_unused_addresses_by_watchlabel(self, label, *count):
        """Get adresse unused by watch label
label [count]"""
        call = 'get_unused_addresses_by_watchlabel'
        if count:
            endpoint = "{}/{}/{}/{}".format(self.url, call, label, count)
        else:
            endpoint = "{}/{}/{}".format(self.url, call, label)
        response = self.get_data(call, endpoint)
        return response
    # Get request with argument(s)
    def getblockhash(self, height): ## Return a string not a json
        """Get the block hash on a specific height
height"""
        call = 'getblockhash'
        endpoint = "{}/{}/{}".format(self.url, call, height)
        response = self.get_data(call, endpoint)
        return response
    def unwatch(self, address):
        """Remove an address from the watch list
address"""
        call = 'unwatch'
        endpoint = "{}/{}/{}".format(self.url, call, address)
        response = self.get_data(call, endpoint)
        return response
    def unwatchxpubbyxpub(self, xpub):
        """Remove an xpub from watch list using xpub
xpub"""
        call = 'unwatchxpubbyxpub'
        endpoint = "{}/{}/{}".format(self.url, call, xpub)
        response = self.get_data(call, endpoint)
        return response
    def unwatchxpubbylabel(self, label):
        """Remove an xpub from watch list using label
label"""
        call = 'unwatchxpubbylabel'
        endpoint = "{}/{}/{}".format(self.url, call, label)
        response = self.get_data(call, endpoint)
        return response
    def getactivewatchesbyxpub(self, xpub):
        """Get a list of address watches by xpub
xpub"""
        call = 'getactivewatchesbyxpub'
        endpoint = "{}/{}/{}".format(self.url, call, xpub)
        response = self.get_data(call, endpoint)
        return response
    def getactivewatchesbylabel(self, label):
        """Get a list of address watches by label
label"""
        call = 'getactivewatchesbylabel'
        endpoint = "{}/{}/{}".format(self.url, call, label)
        response = self.get_data(call, endpoint)
        return response
    def getblockinfo(self, block):
        """Get block informations by block hash
hash"""
        call = 'getblockinfo'
        endpoint = "{}/{}/{}".format(self.url, call, block)
        response = self.get_data(call, endpoint)
        return response
    def gettransaction(self, txid):
        """Get transactions informations by txid
txid"""
        call = 'gettransaction'
        endpoint = "{}/{}/{}".format(self.url, call, txid)
        response = self.get_data(call, endpoint)
        return response
    def ln_decodebolt11(self, bolt11):
        """Decode bolt11 lightning invoice string
bolt11"""
        call = 'ln_decodebolt11'
        endpoint = "{}/{}/{}".format(self.url, call, bolt11)
        response = self.get_data(call, endpoint)
        return response
    def getbalancebyxpub(self, xpub):
        """Get balance of address watches by xpub 
xpub"""
        call = 'getbalancebyxpub'
        endpoint = "{}/{}/{}".format(self.url, call, xpub)
        response = self.get_data(call, endpoint)
        return response
    def getbalancebyxpublabel(self, label):
        """Get balance of address watches by label
label"""
        call = 'getbalancebyxpublabel'
        endpoint = "{}/{}/{}".format(self.url, call, label)
        response = self.get_data(call, endpoint)
        return response
    def ots_getfile(self, hashing):
        "hash"
        call = 'ots_getfile'
        endpoint = "{}/{}/{}".format(self.url, call, hashing)
        response = self.get_data(call, endpoint)
        return response
    def ln_getinvoice(self, label):
        "label"
        call = 'ln_getinvoice'
        endpoint = "{}/{}/{}".format(self.url, call, label)
        response = self.get_data(call, endpoint)
        return response
    def ln_delinvoice(self, label):
        "label"
        call = 'ln_delinvoice'
        endpoint = "{}/{}/{}".format(self.url, call, label)
        response = self.get_data(call, endpoint)
        return response
    # Post requests
    def watch(self, address, cburl0=None, cburl1=None, emsg=None):
        """Add bitcoin address to watches list
address [unconfirmedCallbackURL confirmedCallbackURL eventMessage]"""
        call = 'watch'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"address":address, "unconfirmedCallbackURL":cburl0, \
            "confirmedCallbackURL":cburl1, "eventMessage":emsg}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def watchxpub(self, xpub, label=None, path="0/n", \
        nstart=0, cburl0=None, cburl1=None): # "0/1/n" electrum = 0/n(receiving) 1/n(change)
        """Add xpub to watches list
xpub [label path nstart unconfirmedCallbackURL confirmedCallbackURL]"""
        call = 'watchxpub'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"label":label, "pub32":xpub, "path":path, "nstart":int(nstart), \
            "unconfirmedCallbackURL":cburl0, "confirmedCallbackURL":cburl1}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def watchtxid(self, txid, cburl1=None, xcburl=None, xconf=6):
        """Add transaction ID to watches list
txid [cburl xcburl xconf]"""
        call = 'watchtxid'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"txid":txid, "confirmedCallbackURL":cburl1, \
            "xconfCallbackURL":xcburl, "nbxconf":int(xconf)}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def spend(self, address, amount, emsg=None):
        """Spend from spender wallet
address amount [eventMessage]"""
        call = 'spend'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"address":address, "amount":amount, "eventMessage":emsg}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def bumpfee(self, txid, conf_target):
        """Add fees to a transaction to execute it in X block
txid confTarget"""
        call = 'bumpfee'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"txid":txid, "confTarget":conf_target}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def addtobatch(self, address, amount):
        """Add a spend from spender wallet to batching
address amount"""
        call = 'addtobatch'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"address":address, "amount":amount}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def derivepubpath(self, xpub, path):
        """Get a list of bitcoin address from an xpub
xpub path"""
        call = 'derivepubpath'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"pub32":xpub, "path":path}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def deriveindex(self, index):
        """Get a list of bitcoin address from an xpub
xpub path"""
        call = 'deriveindex'
        endpoint = "{}/{}/{}".format(self.url, call, index)
        response = self.get_data(call, endpoint, payload)
        return response
    def ln_create_invoice(self, msatoshi, label=None, description=None, cburl=None, expiry=900):
        """Create a lightning bolt11 invoice
msatoshi [label description callbackUrl expiry]"""
        call = 'ln_create_invoice'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"msatoshi":msatoshi, "label":label, "description":description, \
            "expiry":expiry, "callbackUrl":cburl}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def ln_pay(self, bolt11, expected_msatoshi, expected_description):
        """Pay a lightning bolt11 invoice
bolt11 expected_msatoshi expected_description"""
        call = 'ln_pay'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"bolt11":bolt11, "expected_msatoshi":expected_msatoshi, \
            "expected_description":expected_description}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def ln_withdraw(self, address, satoshi=None, feerate="normal", withdrawall="false"):
        """Withdraw from lightning to bitcoin address
address [satoshi feerate withdrawall]"""
        call = 'ln_withdraw'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"destination":address, "satoshi":satoshi, \
            "feerate":feerate, "all":withdrawall}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def ln_connectfund(self, url, msatoshi, cburl=None):
        """Create a channel with an other lightning node
peer msatoshi [callbackUrl]"""
        call = 'ln_connectfund'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"peer":url, "msatoshi":msatoshi, "callbackUrl":cburl}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def ots_stamp(self, hash, cburl=None):
        """Timestamp the hash of a file
hash [callbackUrl]"""
        call = 'ots_stamp'
        endpoint = "{}/{}".format(self.url, call)
        payload = {"hash":hashing, "callbackUrl":cburl}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def ots_verify(self, hash, *base64otsfile):
        """Verify a timestamp file
hash [base64otsfile]"""
        call = 'ots_verify'
        endpoint = "{}/{}".format(self.url, call)
        if base64otsfile:
            payload = {"hash":hashing, "base64otsfile":base64otsfile}
        else:
            payload = {"hash":hashing}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    def ots_info(self, hash=None, *base64otsfile):
        """Get timestamp information
[hash [base64otsfile]"""
        call = 'ots_info'
        endpoint = "{}/{}".format(self.url, call)
        if base64otsfile:
            payload = {"hash":hashing, "base64otsfile":base64otsfile}
        else:
            payload = {"hash":hashing}
        payload = json.dumps(payload)
        response = self.post_data(call, endpoint, payload)
        return response
    # Callbacks requests
    def conf(self):##########
        """Not working, for internal use only"""
        print(self.conf.__doc__)
        #call = 'conf'
        #endpoint = "{}/{}".format(self.url, call)
        #response = self.get_data(call, endpoint)
        #return response
    def newblock(self):##########
        """Not working, for internal use only"""
        print(self.newblock.__doc__)
        #call = 'newblock'
        #endpoint = "{}/{}".format(self.url, call)
        #response = self.get_data(call, endpoint)
        #return response
    def executecallbacks(self):###########
        """Not working, for internal use only"""
        print(_self.executecallbacks._doc__)
        #call = 'executecallbacks'
        #endpoint = "{}/{}".format(self.url, call)
        #response = self.get_data(call, endpoint)
        #return response
    def ots_backoffice(self):#########
        """Not working, for internal use only"""
        print(self.ots_backoffice.__doc__)
        #call = 'ots_backoffice'
        #endpoint = "{}/{}".format(self.url, call)
        #response = self.get_data(call, endpoint)
        #return response

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
        headers = ''
        if response_code == 200:
            headers += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            headers += 'HTTP/1.1 404 Not Found\n'
        headers += "Content-Type: application/json\n"
        headers += 'Content-Length: {}\n\n'.format(lenght)
        return headers
    def service_connection(self, key, mask):
        """Execute actions on incomming callbacks"""
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += recv_data
            else:
                #print("closing connection to", data.addr)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                request = None
                self.callback = None
                #print('Data = {}'.format(data.outb))
                request_re = re.compile(b'POST /(.*) ')
                if request_re.search(data.outb):
                    request = request_re.search(data.outb).group(1)
                    request = request.decode('utf-8')
                    #print('request = {}'.format(request))
                json_re = re.compile(b'{(.*)}')
                if json_re.search(data.outb):
                    self.callback = json_re.search(data.outb).group(1)
                    self.callback = self.callback.decode('utf-8')
                    self.callback = '{}{}{}'.format("{", self.callback, "}")
                    self.callback = json.loads(self.callback)
                    self.callback = json.dumps(self.callback)
                    #print(callback)
                if request:
                    try:
                        response = eval('self.{}()'.format(request))
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
