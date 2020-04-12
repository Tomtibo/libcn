from libcn.libcn import CypherNode
#with config file defined at ~/.cn/cn.conf
cn = CypherNode()
def list_testnet_watch():
    chain = cn.getblockchaininfo()['chain']
    if chain == 'test':
        watch = cn.getactivewatches()['watches']
        for w in watch:
            print(w['address'])
def remove_all_testnet_watch():
    chain = cn.getblockchaininfo()['chain']
    if chain == 'test':
        watch = cn.getactivewatches()['watches']
        for w in watch:
            print(w['address'])
            cn.unwatch(w['address'])
list_testnet_watch()