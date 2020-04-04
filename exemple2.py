from libcn.libcn import CypherNode
def exec():
#    Defined in a non default config file location
    config = "/path/to/config/file/cn.conf"
    cn = CypherNode(configfile=config)
#    Defined with object arguments
#    cn = CypherNode(cnid='002', key='6aeryghaerysertyuhsretytse1xstr+6451lkszDFG456584sdz', url='https://url:2009/v0')
    chain = cn.getblockchaininfo()['chain']
    print(chain)
    balance = cn.getbalancebyxpublabel('Electrum_receiving')['balance']
    sat = float(balance) * 100000000
    print("{} Satoshi".format(int(sat)))
    balance = format(balance, '.8f')
    print("{} ₿".format(balance))
#    waddr = cn.getactivewatches()
#    bbh = cn.getbestblockhash()
exec()
