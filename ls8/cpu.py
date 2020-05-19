"""CPU functionality."""

import sys

# We need LDI, PRN, and HLT
LDI = 0b10000010  # Set Value
PRN = 0b01000111  # Print Value
HLT = 0b00000001  # Stop CPU

# Registry, Memory/RAM, Program Counter needed

# Need a way to write to RAM
# Need a way to read RAM

# Ram holds instructions
# Registry holds values
"""
MAR: Memory Address Register, holds the memory address we're reading or writing
This is the spot in the register where we are reading/writing

MDR: Memory Data Register, holds the value to write or the value just read
This is the value of what we are reading/writing in the register

MAR will take in a register location as an argument (self, reg_num)
MDR will take in a register location and a value (self, reg_num, value)
"""


class CPU:
	"""Main CPU class."""

	def __init__(self):
		self.reg = [0] * 8
		self.ram = [0] * 256
		self.pc = 0

	def ram_read(self, reg_num):  # Take in a register location to read
		returned_value = self.ram[reg_num]  # Set returned_value to be returned to what is index there within the RAM
		return returned_value  # Return the value

	def ram_write(self, reg_num, value):  # Take in a register location to write a value to
		self.ram[reg_num] = value  # At the ram index, set that index to the value passed in

	def load(self):
		"""Load a program into memory."""

		address = 0

		# For now, we've just hardcoded a program:

		program = [
			# From print8.ls8
			0b10000010,  # LDI R0,8; Save value at...
			0b00000000,  # ...R0
			0b00001000,  # The value of 8
			0b01000111,  # PRN R0; Print...
			0b00000000,  # ... what's at R0
			0b00000001,  # HLTl; Stop program
		]

		for instruction in program:
			self.ram[address] = instruction
			address += 1

	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.reg[reg_a] += self.reg[reg_b]
		# elif op == "SUB": etc
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"TRACE: %02X | %02X %02X %02X |" % (
			self.pc,
			# self.fl,
			# self.ie,
			self.ram_read(self.pc),
			self.ram_read(self.pc + 1),
			self.ram_read(self.pc + 2)
		), end='')

		for i in range(8):
			print(" %02X" % self.reg[i], end='')

		print()

	def run(self):
		running = True
		while running:
			command = self.ram[self.pc]  # Current command
			a = self.ram_read(self.pc + 1)  # Passes into ram_read the register index to be read after the command
			b = self.ram_read(self.pc + 2)  # Passes into ram_read the value to be found
			if command == LDI:
				self.reg[a] = b
				self.pc += 3
			elif command == PRN:
				print(self.reg[a])
				self.pc += 2
			elif command == HLT:
				running = False
			else:
				print("Command Unknown")
				break
