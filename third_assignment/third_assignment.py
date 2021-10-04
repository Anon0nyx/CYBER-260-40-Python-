# Author: Dylan
# Course: CYBER-260-40
# Program: Parse through a Master Boot Record and print out the status byte, partition byte, and the first sector address
# Date: Sept 14th, 2021
import struct

def main():
	mbr = bytearray()
	# Attempt to open the MDR file and read the first 512 bytes
	try:
		with open('block.dd', 'rb') as binary_file:
			mbr = binary_file.read(512)
	except IOError as e:
		print('File unable to be opened due to error: ' + str(e))
		return 1

	# Print the byte that is the status flag (0x80)
	print("Status flag(hex): " + str(hex(mbr[0x1BE])))

	# Print the byte that is the partition type (0x83, Linux native file systems)
	print('Partition type(hex): ' + str(hex(mbr[0x1C2])))

	# The starting address of the first sector is stored in a 4 byte memory slot 
	# starting at the address 0x1C6
	result = struct.unpack('<I', mbr[0x1C6:0x1CA])
	print('First sector address(int): ' + str(result[0]))

	return 0

if __name__ == '__main__':
	main()
