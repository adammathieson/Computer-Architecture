import sys
​
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3   # equivalent to LDI in the LS-8
PRINT_REG = 4
PUSH = 5
POP = 6
CALL = 7
RET = 8
​
memory = [0] * 256
​
register = [0] * 8  # Like variables, fixed number of them, fixed names R0 R1 R2 ... R7
​
pc = 0  # Program Counter, current index, pointer to currently executing instruction
halted = False
​
SP = 7
​
register[SP] = 0xf4  # initialize SP to empty stack
​
#------------
# Load memory
#------------
​
if len(sys.argv) != 2:
	print("usage: comp.py filename")
	sys.exit(1)
​
progname = sys.argv[1]
​
address = 0
​
with open(progname) as f:
	for line in f:
		line = line.split("#")[0]
		line = line.strip()  # lose whitespace
​
		if line == '':
			continue
​
		val = int(line) # LS-8 uses base 2!
		#print(val)
​
		memory[address] = val
		address += 1
​
#------------
# Run the CPU
#------------
​
while not halted:
	instruction = memory[pc]
​
	if instruction == PRINT_BEEJ:
		print("Beej!")
		pc += 1
​
	elif instruction == SAVE_REG:
		value = memory[pc + 1]
		reg_num = memory[pc + 2]
​
		register[reg_num] = value
​
		pc += 3
​
	elif instruction == PRINT_REG:
		reg_num = memory[pc + 1]
		print(register[reg_num])
​
		pc += 2
​
	elif instruction == PUSH:
		register[SP] -= 1  # decrement sp
		reg_num = memory[pc + 1]
		reg_val = register[reg_num]
		memory[register[SP]] = reg_val  # copy reg value into memory at address SP
​
		pc += 2
​
	elif instruction == POP:
		val = memory[register[SP]]
		reg_num = memory[pc + 1]
		register[reg_num] = val  # copy val from memory at SP into register
​
		register[SP] += 1  # increment SP
​
		pc += 2
​
	elif instruction == CALL:
		# push return addr on stack
		return_address = pc + 2
		register[SP] -= 1  # decrement sp
		memory[register[SP]] = return_address
​
		# set the pc to the value in the register
		reg_num = memory[pc + 1]
		pc = register[reg_num]
​
	elif instruction == RET:
		# pop the return address off stack
		# store it in the pc
		pc = memory[register[SP]]
		register[SP] += 1
​
	elif instruction == HALT:
		halted = True
		pc += 1
​
	else:
		print(f"Unknown instruction at index {pc}")
		sys.exit(1)