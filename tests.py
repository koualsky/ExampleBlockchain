from unittest import TestCase
from unittest.mock import patch
from block import Blockchain, Buffer


# Unittests


# class BlockTestCase(TestCase):
#     def test_some_test(self):
#         self.assertEqual(1, 1)
#
#
# class BlockchainTestCase(TestCase):
#     def test_example(self):
#         self.assertEqual(1, 1)
#
#
# class BufferTestCase(TestCase):
#     def test_example(self):
#         self.assertEqual(1, 1)


# TDD - Use Cases


class AddingTransactionsToTheBuffer(TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.buffer = Buffer(self.blockchain)

    def test_add_transaction_to_the_buffer(self):
        self.buffer.add('1 transaction')
        self.assertEqual(self.buffer._transactions, ['1 transaction'])

    def test_add_5_transactions_to_the_buffer_in_2_steps(self):
        self.buffer.add('1 transaction', '2 transaction')
        self.buffer.add('3 transaction', '4 transaction', '5 transaction')
        self.assertEqual(self.buffer._transactions, [
            '1 transaction',
            '2 transaction',
            '3 transaction',
            '4 transaction',
            '5 transaction'
        ])


class TestCreateBlockInBlockchain(TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.buffer = Buffer(self.blockchain)

    def test_generate_block_in_blockchain(self):
        self.buffer.add('1 transaction', '2 transaction')
        self.buffer.add('3 transaction')
        self.assertEqual(len(self.blockchain), 0)
        self.buffer.generate_block()
        created_block = self.blockchain[0]
        self.assertEqual(self.buffer._transactions, [])
        self.assertEqual(len(self.blockchain), 1)
        self.assertEqual(created_block.block_number, 0)
        self.assertEqual(created_block.prev_block_hash, 'Init block')
        self.assertEqual(created_block.block_hash, '67c037b2df4867a98bd4583a93dac0b638200254f73c161915bc0da22d338ed6')
        self.assertEqual(created_block.body, ['1 transaction', '2 transaction', '3 transaction'])

    def test_generate_two_blocks_in_blockchain(self):
        self.buffer.add('1 transaction')
        self.buffer.generate_block()
        self.buffer.add('2 transaction')
        self.buffer.generate_block()
        self.assertEqual(len(self.blockchain), 2)
        first_block = self.blockchain[0]
        second_block = self.blockchain[1]
        self.assertEqual(first_block.block_number, 0)
        self.assertEqual(second_block.block_number, 1)
        self.assertEqual(first_block.prev_block_hash, 'Init block')
        self.assertEqual(first_block.block_hash, '3f0fb854adbf267f39bff4842d8e1d3599df154d759b4150543816f5d6217f40')
        self.assertEqual(second_block.prev_block_hash, '3f0fb854adbf267f39bff4842d8e1d3599df154d759b4150543816f5d6217f40')
        self.assertEqual(second_block.block_hash, 'dbc254f2a2cd2e066a36ba5e41a29d815e8d2fdd23957db638deb24f075d0723')
        self.assertEqual(first_block.body, ['1 transaction'])
        self.assertEqual(second_block.body, ['2 transaction'])

    def test_generate_five_blocks_in_blockchain(self):
        self.buffer.add('1 transaction')
        self.buffer.generate_block()
        self.buffer.add('2 transaction')
        self.buffer.generate_block()
        self.buffer.add('3 transaction')
        self.buffer.generate_block()
        self.buffer.add('4 transaction')
        self.buffer.generate_block()
        self.buffer.add('5 transaction')
        self.buffer.generate_block()


        self.assertEqual(len(self.blockchain), 5)
        first_block = self.blockchain[0]
        second_block = self.blockchain[1]
        self.assertEqual(first_block.block_number, 0)
        self.assertEqual(second_block.block_number, 1)
        self.assertEqual(first_block.prev_block_hash, 'Init block')
        self.assertEqual(first_block.block_hash, '3f0fb854adbf267f39bff4842d8e1d3599df154d759b4150543816f5d6217f40')
        self.assertEqual(second_block.prev_block_hash, '3f0fb854adbf267f39bff4842d8e1d3599df154d759b4150543816f5d6217f40')
        self.assertEqual(second_block.block_hash, 'dbc254f2a2cd2e066a36ba5e41a29d815e8d2fdd23957db638deb24f075d0723')
        self.assertEqual(first_block.body, ['1 transaction'])
        self.assertEqual(second_block.body, ['2 transaction'])


class TestIntegrity(TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.buffer = Buffer(self.blockchain)
        self.buffer.add('1 transaction')
        self.buffer.generate_block()
        self.buffer.add('2 transaction')
        self.buffer.generate_block()
        self.buffer.add('3 transaction')
        self.buffer.generate_block()
        self.blockchain.save_chain()

    # fixme - this test overwrites blockchain.txt
    def test_edit_one_block(self):
        self.blockchain._blocks[1]._transactions[0] = 'aaa'
        self.assertEqual(self.blockchain.check_integrity(), False)
        self.assertEqual(self.blockchain.save_chain(), 'Inconsistent blockchain')

    # fixme - this test overwrites blockchain.txt
    def test_add_new_block(self):
        self.buffer.add('4 transaction')
        self.buffer.generate_block()
        self.assertEqual(self.blockchain.check_integrity(), True)
        self.assertEqual(self.blockchain.save_chain(), None)
