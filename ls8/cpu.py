"""CPU functionality."""

import sys

operands = {
    "HLT_op": 0b00000001,
    "LDI_op": 0b10000010,
    "PRN_op": 0b01000111

}

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram =[0] * 256
        self.reg= [NONE] * 8
        self.pc = 0

    # * `MAR`: Memory Address Register -- which memory address we're reading and writing
    # * `MDR`: Memory Data Register --  writes the held or read value

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        return self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def run(self ):
        """Run the CPU."""
        ir = self.ram[self.pc] # read the memory address that's stored in register `PC`, and store that result in `IR`

        # Set up basic pointers
        # * `HLT`: halt the CPU and exit the emulator.
        HLT = 1
        # * `LDI`: load "immediate", store a value in a register, or "set this register to this value".
        LDI = 10000010
        # * `PRN`: a pseudo-instruction that prints the numeric value stored in a   register.
        PRN = 1000111

        operand_a = self.ram_read(self.pc + 1) # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables 
        operand_b = self.ram_read(self.pc + 2) # `operand_a` and `operand_b` in case the instruction needs them.

        # Convert ir to a string so we can check its length easily
        str_ir = str(ir)

        while self.ram[self.pc] != HLT:

            if self.ram[self.pc] == LDI:
                self.ldi(self.ram[self.pc+1], self.ram[self.pc+2])
                self.pc += 2
            elif self.ram[self.pc] == PRN:
                self.prn(self.ram[self.pc+1])
                self.pc +=1

            self.pc += 1