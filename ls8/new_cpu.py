"""CPU functionality."""

import sys

PRN = 1000111
LDI = 10000010 
ADD = 10100000
MUL = 10100010
PUSH = 1000101 
POP = 1000110 
HLT = 1
CALL = 1010000
RET = 10001
CMP = 10100111
JMP = 1010100
JEQ = 1010101
JNE = 1010110
AND = 10101000
OR = 10101010
XOR = 10101011
NOT = 1101001
SHL = 10101100
SHR = 10101101
MOD = 10100100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Clear Ram, and set it equal to the Interrupt vector
        self.ram =[0] * 0xFF
        # Create 8 individual spaces inside a list for the register
        self.reg = [0] * 8
        # Set the register's 7th index to 0xF4
        self.reg[7] = 0xF4
        # Set pc pointer to 0
        self.pc = 0
        # Create the flag pointer, we need a list of 8 empty paces
        self.fl = [0]*8
        self.dispatch_table = {
            LDI: self.ldi,
            PRN: self.prn,
            PUSH: self.push,
            POP: self.pop,
            MUL: self.alu,
            ADD: self.alu,
            CALL: self.call,
            RET: self.pop_off_of_stack,
            CMP: self.alu,
            JMP: self.jump,
            JEQ: self.jump_similarity,
            JNE: self.jump_not_similar,
            CMP: self.alu,
            AND: self.alu,
            OR: self.alu,
            XOR: self.alu,
            NOT: self.alu,
            SHL: self.alu,
            SHR: self.alu,
            MOD: self.alu
        }
        self.alu_dispatch_table = {
            ADD: self.add,
            MUL: self.mul,
            CMP: self.comp,
            AND: self.bitwise_and,
            OR: self.bitwise_or,
            XOR: self.bitwise_xor,
            NOT: self.bitwise_not
        }

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
                    if break_line_strip == '':
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

    def alu(self, reg_a, reg_b):
        """ALU operations."""
        ir = self.ram[self.pc]
        if ir in self.alu_dispatch_table:
            self.alu_dispatch_table[ir](operand_a, operand_b)
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

    def pop_off_of_stack(self):
        # Assign the stack pointer address to the stack pointer
        sp = self.reg[7]

        # higher_value is what will be popped off
        higher_value = self.ram[sp]
        
        # Increment stack pointer
        self.reg[7] += 1

        # Assign self.pc to higher_value so it can be popped off
        self.pc = higher_value
    
    def call(self, number):
        # Get the value within the register using number as the index value
        value = self.reg[number]

        # Point to a later value in the stack
        higher_value = self.pc+2

        # Decrement stack pointer
        self.reg[7] -= 1

        # Assign the stack pointer address to the stack pointer
        sp = self.reg[7]

        # Assing the higher_value a place on the stack according to the index value of the stack pointer
        self.ram[sp] = higher_value
        
        # Jump to the address within the register
        self.pc = value


    def push(self, number):
        # Decrease stack pointer
        self.reg[7] -= 1

        # Use the provided number as the index to get a value from the register
        value = self.reg[number]

        # Assign the stack pointer address to the stack pointer
        sp = self.reg[7]
        
        # Reassign the ram index value of stack pointer equal to what value is
        self.ram[sp] = value

        # Increment self.pc
        self.pc += 2
    
    def pop(self, operand_a):
        # Establish the stack pointer
        sp = self.reg[7]

        # Use the stack pointer as the index to get a value from ram
        value = self.ram[sp]

        # Reassign the reg index value of operand_a equal to what value is
        self.reg[operand_a] = value

        # Increment stack pointer
        self.reg[7] += 1

        # Increment self.pc
        self.pc += 2

    # Create a function to find the index
    def find_idx(self, binary):
        binary_str = str(binary)
        binary_str.replace("0b", '')
        # Converts this into a base two number
        return int(binary_str, 2) 

    # Create a function for the LDI
    def ldi(self, number, value):
        idx = self.find_idx(number)
        self.reg[idx] = value
        self.pc += 3

    # Create a function for the PRN
    def prn(self, number):
        idx = self.find_idx(number)
        print(self.reg[idx])
        self.pc += 2

    def add(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]
        self.pc += 3

    def mul(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]
        self.pc += 3

    def comp(self, reg_a, reg_b):
        self.fl[5] = 0
        self.fl[6] = 0
        self.fl[7] = 0
        if self.reg[reg_a] < self.reg[reg_b]:
            self.fl[5] = 1
        elif self.reg[reg_a] > self.reg[reg_b]:
            self.fl[6] = 1
        elif self.reg[reg_a] == self.reg[reg_b]:
            self.fl[7] = 1
        self.pc += 3

    def bitwise_and(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        self.pc += 3

    def bitwise_or(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        self.pc += 3

    def bitwise_xor(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        self.pc += 3

    def bitwise_not(self, reg_a, not_used):
        self.reg[reg_a] = ~self.reg[reg_a]
        self.pc += 2

    def jump(self, number, not_used):
        address = self.reg[number]
        self.pc = address
    
    def jump_similarity(self, number, not_used):
        if self.fl[7] == 1:
            self.jump(number, not_used)
        elif self.fl[7] == 0:
            self.pc += 2

    def jump_not_similar(self, number, not_used):
        if self.fl[7] == 0:
            self.jump(number, not_used)
        elif self.fl[7] == 1:
            self.pc += 2

    # Structure the run function
    def run(self ):
        """Run the CPU."""
        
        

        # # Convert the IR to string
        # ir_string = str(ir)
        
        # # Set up basic pointers
        # # * `HLT`: halt the CPU and exit the emulator.
        # HLT = 0b00000001
        # # * `LDI`: load "immediate", store a value in a register, or "set this register to this value".
        # LDI = 0b10000010
        # # * `PRN`: a pseudo-instruction that prints the numeric value stored in a   register.
        # PRN = 0b01000111

        # # Convert ir to a string so we can check its length easily
        # ir_string = str(ir)


       
        
        while ir != HLT:
            ir = self.ram[self.pc] # read the memory address that's stored in register `PC`, and store that result in `IR`

            
            operand_a = self.find_idx(self.ram_read(self.pc + 1)) # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables 
            operand_b = self.find_idx(self.ram_read(self.pc + 2)) # `operand_a` and `operand_b` in case the instruction needs them.

            self.dispatch_table[ir](operand_a, operand_b)
            ir = self.ram[self.pc]