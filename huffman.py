import heapq
import os
from functools import total_ordering
import estimate_entropy
from functools import partial

@total_ordering
class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

	# defining comparators less_than and equals
	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	# functions for compression:

	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, file_input, byte_count=4):
		encoded_text = ""
		records = iter (partial (file_input.read, byte_count), b'')
		for r in records:
			r_int = int.from_bytes (r, byteorder='big')  # 将 byte转化为 int
			encoded_text += self.codes[r_int]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self,byte_count=4):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".cmp"

		input = open(self.path, 'rb')
		output = open(output_path, 'wb')
#			text = file.read()
#			text = text.rstrip()

#			frequency = self.make_frequency_dict(text)

		(count, frequency) = estimate_entropy.find_symbol_frequency_dict(input, byte_count)
		self.make_heap(frequency)
		self.merge_nodes()
		self.make_codes()
		input.close()

		input = open(self.path, 'rb')
		encoded_text = self.get_encoded_text(input,byte_count)
		padded_encoded_text = self.pad_encoded_text(encoded_text)
		input.close()

		b = self.get_byte_array(padded_encoded_text)
		output.write(bytes(b))

		print("Compressed")
		return output_path


	""" functions for decompression: """


	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = list('1'*len(encoded_text))
		i = 0
		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				print (character)
				decoded_text[i] = character
				current_code = ""
				i += 1
		decoded_text = decoded_text[:(-i-1)]

		return decoded_text


	def decompress(self, input_path, byte_count=4):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".bin"

		with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
			bit_string = ""

			records = iter (partial (file.read, 1), b'')
			for byte in records:
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
			# byte = file.read(1)
			# while(len(byte) > 0):
			# 	byte = ord(byte)
			# 	bits = bin(byte)[2:].rjust(8, '0')
			# 	bit_string += bits
			# 	byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)
			# tmp = open(r"E:\2.txt",'w')
			# tmp.write(encoded_text)
			# tmp.close()
			# print (encoded_text)
			decompressed_text = self.decode_text(encoded_text)
			result = bytearray()
			result.join(bytearray(int(x)) for x in encoded_text)
			output.write(result)
		print("Decompressed")
		return output_path