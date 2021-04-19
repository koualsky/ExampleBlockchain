import hashlib
import json
import os
import sys


class Block:
    def __init__(self, prev_block_hash: str, block_number: int, transactions: list):
        self._transactions = transactions
        self._block_number = block_number
        self._prev_block_hash = prev_block_hash
        self._block_hash = self.calculate_hash()

    def calculate_hash(self):
        hash_string = '-'.join(self._transactions) + self._prev_block_hash + str(self._block_number)
        hash_encoded = json.dumps(hash_string).encode()
        return hashlib.sha256(hash_encoded).hexdigest()

    @property
    def block_number(self):
        return self._block_number

    @property
    def prev_block_hash(self):
        return str(self._prev_block_hash)

    @property
    def block_hash(self):
        return str(self.calculate_hash())

    @property
    def header(self):
        return {
            'block_number': self._block_number,
            'prev_block_hash': self.prev_block_hash,
            'block_hash': self.block_hash
        }

    @property
    def body(self):
        return self._transactions


class Blockchain:
    def __init__(self):
        self._blocks = []

    def add(self, block: Block):
        self._blocks.append(block)

    def __len__(self):
        return len(self._blocks)

    def __getitem__(self, index):
        return self._blocks[index]

    @property
    def chain(self):
        return [block.block_hash for block in self._blocks]

    def stats(self):
        _numb_of_blocks = str(len(self._blocks))
        _total_size_in_bytes = str(sys.getsizeof(self._blocks))
        print(f'''
        Number of blocks: {_numb_of_blocks}
        Total size in bytes: {_total_size_in_bytes}
        ''')

    def check_integrity(self) -> bool:
        # Old blocks
        _old_blocks_hash = []
        with open('blockchain.txt', 'r') as f:
            for line in f:
                header, body = line[:-1].split('~')
                block_number, prev_block_hash = header.split('.')
                transactions = body.split('$')
                _old_blocks_hash.append(Block(prev_block_hash, int(block_number), transactions).calculate_hash())

        # New blocks
        _new_blocks_hash = []
        for block in self._blocks:
            _new_blocks_hash.append(block.calculate_hash())
        if _old_blocks_hash < _new_blocks_hash:
            n = len(_new_blocks_hash) - len(_old_blocks_hash)
            return _old_blocks_hash == _new_blocks_hash[:-n]
        else:
            return _old_blocks_hash == _new_blocks_hash

    def save_chain(self):
        if self.check_integrity():
            if os.path.exists('blockchain.txt'):
                os.remove('blockchain.txt')
            for block in self._blocks:
                with open('blockchain.txt', 'a') as f:
                    f.write(str(block.block_number) + '.' + block.prev_block_hash + '~' + '$'.join(block.body) + '\n')
        else:
            return 'Inconsistent blockchain'

    def load_chain(self):
        self._blocks = []
        with open('blockchain.txt', 'r') as f:
            for line in f:
                header, body = line[:-1].split('~')
                block_number, prev_block_hash = header.split('.')
                transactions = body.split('$')
                self._blocks.append(Block(prev_block_hash, int(block_number), transactions))


class Buffer:
    def __init__(self, blockchain: Blockchain):
        self._transactions = []
        self._blockchain = blockchain

    def add(self, *transactions):
        self._transactions += [*transactions]

    def show(self):
        for t in self._transactions:
            print(t)

    def generate_block(self):
        prev_block_hash = self._blockchain[-1].block_hash if self._blockchain else 'Init block'
        block_number = len(self._blockchain)
        block = Block(prev_block_hash, block_number, self._transactions[:])
        self._blockchain.add(block)
        self._transactions.clear()
