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

    def ram_read(self, MAR):
        # should accept the address to read and return the value stored there.
        return self.ram[MAR]


    def ram_write(self, MAR, MDR):
        # should accept a value to write, and the address to write it to. 
        self.ram[MAR] = MDR

    def load(self, program=None):
        """Load a program into memory."""
        # If there are less then two programs entered in the command line
        if len(sys.argv) < 2:
            # Provide user feedback
            sys.exit("We need two file names entered.")

        # For froward thinking, do some error handling
        try:
            # Set the address pointer to 0
            address = 0
            # Open the program as a file
            with open(program) as file:
                # Loop through every line in the file
                for line in file:
                    # Now we need to do some exception handling withing the file
                    ## Split every line when we encounter a hashtag or a python comment 
                    break_line = line.split('#')[0]
                    # Split each word as a list item
                    break_line_strip = break_line.strip()
                    # Check if break_line has no spaces
                    if break_line == '':
                        # If so, continue on
                        continue
                    # Transform the break_line value into an integer
                    break_line_int = int(break_line_strip)
                    # Set the index of address to equal the value of the break_line_int
                    self.ram[address] = break_line_int
                    # Increment address 
                    address += 1

        # If the file is not found
        except FileNotFoundError:
            # Make this user friendly and tell them what went wrong
            sys.exit(f"{sys.argv[0]} and {sys.argv[1]} file's was not found")

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

    # Create a function to find the index
    def find_idx(self, binary):
        binary_str = str(binary)
        binary_str.replace("0b", '')
        return int(binary_str, 2) 

    # Create a function for the LDI
    def ldi(self, number, value):
        idx = self.find_idx(number)
        self.reg[idx] = value

    # Create a function for the PRN
    def prn(self, number):
        idx = self.find_idx(number)
        print(self.reg[idx])

    # Structure the run function
    def run(self ):
        """Run the CPU."""
        ir = self.ram[self.pc] # read the memory address that's stored in register `PC`, and store that result in `IR`

        # Set up basic pointers
        # * `HLT`: halt the CPU and exit the emulator.
        HLT = 0b00000001
        # * `LDI`: load "immediate", store a value in a register, or "set this register to this value".
        LDI = 0b10000010
        # * `PRN`: a pseudo-instruction that prints the numeric value stored in a   register.
        PRN = 0b01000111

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