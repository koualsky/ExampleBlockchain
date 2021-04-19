from block import Blockchain, Buffer


if __name__ == '__main__':
    blockchain = Blockchain()
    buffer = Buffer(blockchain)
    blockchain.load_chain()
    help_text = '''
add \t- add transaction to the buffer
buf \t- show the buffer
gen \t- generate block from transactions in buffer and clean buffer
get \t- get the specific block
stat \t- statistics for blockchain
write \t- write blockchain to disk
load \t- load blockchain from disk
exit \t- close program'''
    s = ''
    print('Type "help" to see all options')
    while s != 'exit':
        s = input('>>> ')

        if s == 'help':
            print(help_text)

        if s == 'add':
            add_s = input('Transaction: ')
            buffer.add(add_s)
            print(f'Transaction "{add_s}" was added to the buffer.')

        if s == 'buf':
            print('TRANSACTIONS IN THE BUFFER:')
            buffer.show()

        if s == 'gen':
            buffer.generate_block()
            print('Block was created.')

        if s == 'get':
            n = int(input('Type specific block number (count from 0): '))
            print(blockchain[n])
            print(f'HEADER: {blockchain[n].header}')
            print(f'BODY: {blockchain[n].body}')

        if s == 'stat':
            print('BLOCKCHAIN STATISTICS:')
            blockchain.stats()

        if s == 'write':
            response = blockchain.save_chain()
            if response == None:
                print('Blockchain was saved.')
            else:
                print(f'{response}')

        if s == 'load':
            blockchain.load_chain()
            print('Blockchain was loaded.')
