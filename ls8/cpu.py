"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
MOD = 0b10100100
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 7
        self.pc = 0
        self.bt = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            ADD: self.ADD,
            MUL: self.MUL,
            MOD: self.MOD,
            POP: self.POP,
            PUSH: self.PUSH,
            CALL: self.CALL,
            RET: self.RET,
            CMP: self.CMP,
            }
        self.halted = False
        self.fl = [0] * 8

        #TODO Setting the reg slot of the sp; does this go here? 
        self.reg[self.sp] = 0xf4

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("Usage: comp.py filename")
            sys.exit(1)

        address = 0

        progname = sys.argv[1]

        with open(progname) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == '':
                    continue
                
                val = int(line, 2)
                # print(val)

                self.ram[address] = val
                address += 1
            # print('end of load')


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == "CMP":
            if reg_a == reg_b:
                self.fl[7] = 1
            elif reg_a < reg_b:
                self.fl[5] = 1
            elif reg_a > reg_b:
                self.fl[6] = 1
        elif op == "MUL":
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
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    
    # Main commands
    def LDI(self, op_a, op_b):
        self.reg[op_a] = op_b
        # print('LDI', self.reg[op_a])
        self.pc += 3

    def PRN(self, op_a, op_b):
        print('PRN', self.reg[op_a])
        self.pc += 2

    def HLT(self, op_a, op_b):
        # print('HLT')
        self.halted = True
        self.pc += 1

    # alu commands
    def ADD(self, op_a, op_b):
        self.alu("ADD", op_a, op_b)
        self.pc += 3

    def MUL(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)
        print("MUL", self.reg[op_a])
        self.pc += 3

    def MOD(self, op_a, op_b):
        if op_b == 0:
            print("Usage: value cannot be 0")
        else:
            self.alu("MOD", op_a, op_b)
            print("MOD", self.reg[op_a])
        self.pc += 2

    def CMP(self, op_a, op_b):
        self.alu("CMP", op_a, op_b)
        self.pc += 3

    # Stack access
    def PUSH(self, op_a, op_b):
        self.reg[self.sp] -= 1
        val = self.reg[op_a]
        self.ram_write(val, self.reg[self.sp])
        # print("PUSH", self.ram_read(self.reg[self.sp]))

        self.pc += 2

    def POP(self, op_a, op_b):
        val = self.ram_read(self.reg[self.sp])
        self.reg[op_a] = val

        self.reg[self.sp] += 1

        # print("POP", val, self.reg[self.sp])
        self.pc += 2

    def CALL(self, op_a, op_b):
        return_address = self.pc + 2
        self.reg[self.sp] -= 1
        self.ram_write(return_address, self.reg[self.sp])

        self.pc = self.reg[op_a]

    def RET(self, op_a, op_b):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def run(self):
        """Run the CPU."""

        while self.halted is False:
            instruction = self.ram[self.pc]
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            if instruction in self.bt:
                self.bt[instruction](op_a, op_b)
            else:
                print(f"Unknown instruction at index {self.pc}")
                sys.exit(1)           






