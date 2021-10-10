# Python-ISA-Compiler
compiler.py was made to take a text file with a set of custom ISA and create a new text file output with the hexadecimal values of each instruction

A small example of the expected input file:

#Test code

MUL R1, R2, R7

.aux1
ADD R1, R2, 85
ADD R5, R3, R13
JGE R2, R4, aux2
JMP aux1

.aux2
SUB R4, R2, R1
STR R9, R15
LD R13, R4
MV R11, R12
