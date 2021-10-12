# Python-ISA-Compiler
compiler.py was made to take a text file with a set of custom ISA and create a new text file output with the binary values of each instruction

The syntax, values of bits for each component of the comple value and number of instructions were defined by the teamgroup.

Each instruction size will be of 32 bits, where opcode its 4 bits size, each register are 6 bits and additional to complete the 32 bits (used mostly on jumps/branches)

Jump and Jump Greater Equal take a list of [[label, line position]] in order to identufy where the other labels for the jumps are located and then assing it to the final value.

A small example of the expected input file will be in the arm.txt file
