from libcn.libcn import CypherNode
#with config file defined at ~/.cn/cn.conf
cn = CypherNode()
chain = cn.getblockchaininfo()['chain']
if chain == 'test':
    watch = cn.getactivewatches()['watches']
    for w in watch:
        print(w['address'])
