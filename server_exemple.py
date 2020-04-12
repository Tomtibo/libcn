from libcn.libcn import CypherNode, CallbackServer

class WaitCallback(CallbackServer):
    """Exemple of using 'CallbackServer' class for handling callbacks to execute actions.
    Each functions must reflect the callbacks url used in cyphernode callbacks config.
    For exemple, a watched address with callback url 'http://url:port/conf' need 
    a function called 'conf' to be handled by this class. The 'return' statement will 
    send the returned value to the coresponding response topîc. If no 'return'
    statement is used, a string value of 'True' is sent. If the function fail or if
    the function do not exist, a string value of 'False' is sent."""
    def __init__(self, port):
        """Initialyse CallbackServer options"""
        self.port = port
    def unconf(self, call):
        """Do stuff with not confirmed paiment callbacks
        fields = ['id', 'address', 'hash', 'vout_n', 'sent_amount', 'confirmations', 'received', 'size', \
            'vsize', 'fees', 'is_replaceable', 'pub32', 'pub32_label', 'pub32_derivation_path', 'eventMessage']"""

        amount = call['sent_amount']
        amount = format(amount, '.8f')
        amount = '{} ₿'.format(amount)
        fees = call['fees']
        fees = format(fees, '.8f')
        fees = '{} ₿'.format(fees)
        #print('Paiment non confirmé = {}'.format(call))
        print('Adresse \'{}\' received {} at {} and the transaction fees is {}'.format(call['address'], amount, call['received'], fees))

    def conf(self, call):
        """Do stuff with confirmed paiment callbacks"
        fields = ['id', 'address', 'hash', 'vout_n', 'sent_amount', 'confirmations', 'received', 'size', \
            'vsize', 'fees', 'is_replaceable', 'pub32', 'pub32_label', 'pub32_derivation_path', 'eventMessage']"""

        amount = call['sent_amount']
        amount = format(amount, '.8f')
        amount = '{} ₿'.format(amount)
        fees = call['fees']
        fees = format(fees, '.8f')
        fees = '{} ₿'.format(fees)
        #print('Paiment non confirmé = {}'.format(call))
        print('Confirmation of adresse \'{}\' received {} at {} and the transaction fees is {}'.format(call['address'], amount, call['received'], fees))

    def txunconf(self, call):
        "Do stuff with unconfirmed transation callbacks"

        print('Transaction non confirmé = {}'.format(call))

    def txconf(self, call):
        "Do stuff with confirmed transaction callbacks"

        print('Transaction confirmé = {}'.format(call))

    def ln_invoice(self, call):
        "Do stuff with lighning invoice callbacks"

        print('Lightning invoice confirmé = {}'.format(call))

    def ln_connect(self, call):
        "Do stuff with lighning connected node callbacks"

        print('lighning connect confirmé = {}'.format(call))

    def ots_stamp(self, call):
        "Do stuff with ots callbacks"

        print('OTS stamp confirmé = {}'.format(call))

wc = WaitCallback(2906)
wc.start()
