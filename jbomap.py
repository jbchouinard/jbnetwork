import time
from jbheap import KeyValueHeap


class OrderedMap(object):
	"""A mutable ordered sequence with optional labels.
	Labels can be any hashable value and must be unique.

	Note that if integers are used as keys, accessing
	by key will not work, since omap[i] where i is an int
	accesses by (positional) index.

	Methods
		append
		insert
		remove
		remove_by_label
		index
		index_by_label

	Supported operators
		+ (concatenates)
		Indexing with []
		Slice indexing with [:]

	 Usage
	 	omap = OMap({(0, 'foo'):'bar', (1, 'baz'):'banana'})
		omap[0]
		 > 'bar'
		omap['foo']
		 > 'bar'
		omap[1] = 'apple'
		omap['baz']
		 > 'apple'

	"""
	def __init__(self, map=None):
		self.omap = []
		self.lmap = KeyValueHeap()

		if map is not None:
			for key in map:
				try:
					self.insert(key[0], key[1], map[key])
				except IndexError:
					self.insert(key[0], None, map[key])

	def __add__(self, operand2):
		pass

	def __len__(self):
		pass

	def __iter__(self):
		pass

	def append(self, val, label=None):
		pass

	def insert(self, ii, val, label=None):
		if not hash(label) in self.lmap.keys():
			self.omap.insert(ii, (val, label))
			if label is not None:
				self.lmap.insert((hash(label), val))
		else:
			raise AttributeError('Label already exists.')

	def remove(self, ii):
		pass
	
	def remove_by_label(self, label):
		pass

	def index(self, ii):
		pass

	def index_by_label(self, label):
		pass
