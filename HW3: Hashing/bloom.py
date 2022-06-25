'''bloom.py defines a bloom filter which is an
approximate set membership data structure. You
will implement a full bloom filter in this module 
'''
import array
import binascii
import random
import string

class Bloom(object):

	def __init__(self, m,k, seed=0):
		'''Creates a bloom filter of size m with k 
		   independent hash functions.
		'''

		self.array = array.array('B', [0] * m)
		self.hashes = self.generate_hashes(m,k,seed)

	'''def generate_hashes_helper(self, st):
				val = binascii.crc32(bytes(str(st),'utf-8')) & 0xffffffff
				return (A * val + B) % (m + 1)'''

	def generate_hashes(self, m, k, seed):
		'''Generate *k* independent linear hash functions 
		   each with the range 0,...,m. 

		   m: the range of the hash functions
		   k: the number of hash functions
		   seed: a random seed that controls which A/B linear 
		   parameters are used.

		   The output of this function should be a list of functions
		'''

		# maximum integer value
		MAXINT = 2**32-1
		random.seed(seed)
		A_B_lst = []
		for i in range(k):
			A = random.randint(0, MAXINT)
			B = random.randint(0, MAXINT)
			A_B_lst.append((A, B))

		func_list = [lambda x, i=i: ((A_B_lst[i][0]) * binascii.crc32(bytes(str(x),'utf-8')) & 0xffffffff + (A_B_lst[i][1])) % m for i in range(k)]
		
		return func_list
		
	def put(self, item):
		'''Add a string to the bloom filter, returns void
		'''
		for j in range(len(self.hashes)):
			i = self.hashes[j](item)
			self.array[i] = 1

	def contains(self, item):
		'''Test to see if the bloom filter could possibly
		contain the string (true (possibly)), false (definitely).
		'''
		for j in range(len(self.hashes)):
			i = self.hashes[j](item)
			if self.array[i] == 0:
				return False
		return True

