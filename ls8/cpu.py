"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.IM = 0
        self.IS = 0
        self.SP = 0
        self.PC = 0 # program counter

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
        print(op, reg_a, reg_b)
        print(self.reg[reg_a], self.reg[reg_b])

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')


    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram[self.PC]

            # arity_bits = f'{IR:08b}'[:2]
            # arity = int(arity_bits, 2)
            arity = IR >> 6
            next_start = self.PC + arity + 1
            args = self.ram[self.PC + 1: next_start]

            if IR == 0x01: # HLT Halt
                quit()
            elif IR == 0x82: # LDI load value B into register A
                self.reg[args[0]] = args[1]
            elif IR == 0x47: # PRN Print
                print(self.reg[args[0]])
            elif IR == 0xA2: # MUL Multiply value in A by value in B
                self.alu('MUL', *args)

            self.PC = next_start

