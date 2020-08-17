"""Exemple of handling callback from cyphernode"""
from libcn.libcn import CallbackServer
import json
class WaitCallback(CallbackServer):
    """Exemple of using 'CallbackServer' class for handling callbacks and execute actions.
    Each functions must reflect the callbacks url used in cyphernode callbacks config.
    For exemple, a watched address with callback url 'http://url:port/conf' need
    a function called 'conf' to be handled by this class. The 'return' statement will
    send the returned value to the coresponding response topîc. If no 'return'
    statement is used, a string value of 'True' is sent. If the function fail or if
    the function do not exist, a string value of 'False' is sent."""
    def __init__(self, port):
        """Initialyse CallbackServer options"""
        #super.__init__(CallbackServer)
        self.port = port
    def unconf(self):
        """Do stuff with not confirmed paiment callbacks
        fields = ['id', 'address', 'hash', 'vout_n', 'sent_amount', \
            'confirmations', 'received', 'size', \
            'vsize', 'fees', 'is_replaceable', 'pub32', \
                'pub32_label', 'pub32_derivation_path', 'eventMessage']"""
        if self.callback:
            call = json.loads(self.callback)
            amount = call['sent_amount']
            amount = format(amount, '.8f')
            amount = '{} ₿'.format(amount)
            fees = call['fees']
            fees = format(fees, '.8f')
            fees = '{} ₿'.format(fees)
            #print('Paiment non confirmé = {}'.format(call))
            print('Adresse \'{}\' received {} at {} and the transaction fees is {}'\
                .format(call['address'], amount, call['received'], fees))

    def conf(self):
        """Do stuff with confirmed paiment callbacks"
        fields = ['id', 'address', 'hash', 'vout_n', 'sent_amount', \
            'confirmations', 'received', 'size', \
            'vsize', 'fees', 'is_replaceable', 'pub32', \
                'pub32_label', 'pub32_derivation_path', 'eventMessage']"""
        if self.callback:
            call = json.loads(self.callback)
            amount = call['sent_amount']
            amount = format(amount, '.8f')
            amount = '{} ₿'.format(amount)
            fees = call['fees']
            fees = format(fees, '.8f')
            fees = '{} ₿'.format(fees)
            #print('Paiment non confirmé = {}'.format(call))
            print('Confirmation of adresse \'{}\' received {} at {} and the transaction fees is {}'\
                .format(call['address'], amount, call['received'], fees))

    def txunconf(self):
        """Do stuff with unconfirmed transation callbacks
        fields = ['id', 'txid', 'confirmations']"""
        if self.callback:
            call = json.loads(self.callback)
            print('Transaction non confirmé = {}'.format(call))

    def txconf(self):
        """Do stuff with confirmed transaction callbacks"
        fields = ['id', 'txid', 'confirmations']"""
        if self.callback:
            call = json.loads(self.callback)
            print('Transaction confirmé = {}'.format(call))

    def ln_invoice(self):
        "Do stuff with lightning invoice callbacks"
        if self.callback:
            call = json.loads(self.callback)
            print('Lightning invoice confirmé = {}'.format(call))

    def ln_connect(self):
        "Do stuff with lightning connected node callbacks"
        if self.callback:
            call = json.loads(self.callback)
            print('lightning connect confirmé = {}'.format(call))

    def ots_stamp(self):
        "Do stuff with ots callbacks"
        if self.callback:
            call = json.loads(self.callback)
            print('OTS stamp confirmé = {}'.format(call))

WCB = WaitCallback(2906)
print('WaitCallback running ....')
WCB.start()
