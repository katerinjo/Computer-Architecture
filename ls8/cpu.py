"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 7 + [256]
        self.PC = 0 # program counter
        self.FL = 0

    @property
    def IM(self):
        return self.reg[5]

    @IM.setter
    def IM(self, val):
        self.reg[5] = val

    @property
    def IS(self):
        return self.reg[6]

    @IS.setter
    def IS(self, val):
        self.reg[6] = val

    @property
    def SP(self):
        return self.reg[7]

    @SP.setter
    def SP(self, val):
        self.reg[7] = val

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program=None):
        """Load a program into ram."""

        address = 0

        # For now, we've just hardcoded a program:

        if program is None:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == 0xA0: # ADD
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 0xA2: # MUL
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 0xA7: # CMP
            self.FL = self.FL & 0b11111000 # clear comparison bits
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL += 0b100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL += 0b010
            else:
                self.FL += 0b001
        else:
            raise Exception(f"Unsupported ALU operation: {op:X}")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: Loc: %02X Vals: %02X %02X %02X  RegVals:" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        print('RAM', *[hex(val)[2:] for val in self.ram[:25]])
        print('STACK', self.ram[self.SP:])


    def run(self):
        """Run the CPU."""
        while True:
            # self.trace()
            # print()
            IR = self.ram[self.PC]

            arity = IR >> 6
            use_alu = IR >> 5 & 1
            sets_pc = IR >> 4 & 1
            next_start = self.PC + arity + 1
            args = self.ram[self.PC + 1: next_start]

            if use_alu:
                self.alu(IR, *args)
            else:
                {
                    0x01: self.HLT,
                    0x11: self.RET,
                    0x45: self.PUSH,
                    0x46: self.POP,
                    0x47: self.PRN,
                    0x50: self.CALL,
                    0x54: self.JMP,
                    0x55: self.JEQ,
                    0x82: self.LDI,
                }[IR](*args)

            if not sets_pc:
                self.PC = next_start

    @staticmethod
    def HLT():
        quit()

    def RET(self):
        self.PC = self.ram[self.SP]
        self.SP += 1

    def PUSH(self, register): # Push onto stack
        self.SP -= 1
        self.ram[self.SP] = self.reg[register]

    def POP(self, register): # Pop from stack
        self.reg[register] = self.ram[self.SP]
        self.SP += 1

    def PRN(self, register): # Print
        print(self.reg[register])

    def CALL(self, register): # Call subroutine
        # self.PUSH(self.PC + 2)
        self.SP -= 1
        self.ram[self.SP] = self.PC + 2
        self.PC = self.reg[register]

    def JMP(self, register): # Jump to address given by register
        self.PC = self.reg[register]

    def JEQ(self, register): # Jump to address given by register if equal flag
        if self.FL & 1:
            self.PC = self.reg[register]
        else:
            self.PC += 2

    def LDI(self, register, val): # Load value B into register A
        self.reg[register] = val

    def MUL(self, valA, valB):
        self.alu('MUL', valA, valB)

