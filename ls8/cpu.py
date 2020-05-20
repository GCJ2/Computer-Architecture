"""CPU functionality."""

import sys

# print(sys.argv)
# print(sys.argv[1])


# We need LDI, PRN, and HLT
# PUSH and POP are needed
# R7 is reserved as the stack pointer (SP)
LDI = 0b10000010  # Set Value
PRN = 0b01000111  # Print Value
HLT = 0b00000001  # Stop CPU
MUL = 0b10100010  # Multiply two registers together
PUSH = 0b01000101  # Push
POP = 0b01000110  # Pop
SP = 7

"""
PUSH:
Push the value in the given register on the stack:

Decrement the SP.
Copy the value in the given register to the address pointed to by SP.

POP:
Pop the value at the top of the stack into the given register:

Copy the value from the address pointed to by SP to the given register.
Increment SP


Per the spec, stack starts at R7/F3
Stack pointer points to what is at the top of the stack
Stack grows down, so pointer decrements when something is added to it
Empty stack points to F3
Stack with one item points to F3
Stack with two items points to F2
"""

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

	def load(self, program):
		"""Load a program into memory."""

		address = 0
		program = program
		print(program)
		with open(program) as f:
			for line in f:
				# print(line)
				command = line.split('#')  # Remove comments
				command = command[0].strip()  # Removes whitespaces
				# print(command)
				# command = int(commands) This makes everything base 10, instead of base 2
				if command == '':  # This just i
					continue
				command = int(command, 2)
				# print(command)
				self.ram[address] = command
				# print(self.ram[address])
				address += 1

		# For now, we've just hardcoded a program:

		program = [

		]

		for instruction in program:
			self.ram[address] = instruction
			address += 1

	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.reg[reg_a] += self.reg[reg_b]
		# elif op == "SUB": etc
		if op == "MUL":
			self.reg[reg_a] *= self.reg[reg_b]
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
			# self.trace()
			command = self.ram[self.pc]  # Current command
			a = self.ram_read(self.pc + 1)  # Passes into ram_read the register index to be read after the command
			b = self.ram_read(self.pc + 2)  # Passes into ram_read the value to be found
			if command == LDI:
				self.reg[a] = b
				# print(f'Added {b} to {self.reg[a]}')
				self.pc += 3
			elif command == PRN:
				print(self.reg[a])
				self.pc += 2
			elif command == MUL:
				self.alu('MUL', a, b)
				self.pc += 3
			elif command == PUSH:
				selected_reg = a  # Find current register
				value = self.reg[selected_reg]  # Get the value out of it
				self.reg[SP] -= 1  # Decrement the stack pointer
				self.ram_write(self.reg[SP], value)  # At the SP location in RAM, add the value from the reg
				self.pc += 2  # Increment by two, as is two-bit OP
			elif command == POP:
				selected_reg = a  # Find selected register
				value = self.ram_read(self.reg[SP])  # Get the value of whatever is stored at the SP
				self.reg[selected_reg] = value  # Set the selected_reg in the register to the value taken from the SP
				self.reg[SP] += 1  # Increment the SP and leave sub behind just like I left Becky behind on read
				self.pc += 2  # Increment PC by two, as POP is a two-bit operation

			elif command == HLT:
				running = False
			else:
				print("Command Unknown")
				break
