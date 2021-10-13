##############################################################################################
'''
Compiler for custom assembly ISA

The program creates a text file with the binary values of the instructions
to be uploaded to the processor (CPU) 

Inputs --> text file with the instructions following the nomenclature
Outputs --> rom.txt file with binary equivalent of the instructions

format --> OPcode (4 bits) + Register Destination (6 bits) + Register 1 (6 bits) + Register 2 (6 bits) + additional for 32 bits

'''
##############################################################################################
import sys
import re
import csv
##############################################################################################
##################                  Variables                               ##################
##############################################################################################

bits = 10 #additional values 
formatbits = "{:06b}"
space = ''
labels = []
lineNumber=1
tok = []

##############################################################################################

def writetext(fn, instruction, b):
    #Output file
	with open("rom.txt", "a") as new_file:
        	new_file.write('{:<30}'.format(str(instruction))+'{:>30}'.format(str(b)+"\n"))

##############################################################################################
##################                  Arithmetic Functions                    ##################
##############################################################################################

#Addition
def ADD(i,parametros): 

    r_bin = []
    for n in range(len(parametros[1:])):
        r=formatbits.format(int(parametros[n+1][1:]))
        r_bin.append(r)
    values=space.join(r_bin)

    comp_line="0001"+space+values+space.zfill(bits)
    writetext("rom.txt", str(i)+". "+",".join(parametros), comp_line)
   
#Substraction
def SUB(i,parametros):

    r_bin = []
    for n in range(len(parametros[1:])):
        r=formatbits.format(int(parametros[n+1][1:]))
        r_bin.append(r)
    values=space.join(r_bin)
    comp_line="0010"+space+values+space.zfill(bits)
    writetext("rom.txt", str(i)+". "+",".join(parametros), comp_line)
       
#Multiplication
def MUL(i,parametros): 
      
    r_bin = []
    for n in range(len(parametros[1:])):
        r=formatbits.format(int(parametros[n+1][1:]))
        r_bin.append(r)
    values=space.join(r_bin)

    comp_line="0011"+space+values+space.zfill(bits)
    writetext("rom.txt", str(i)+". "+",".join(parametros), comp_line) 

##############################################################################################
##################                  Conditional Functions                    ##################
##############################################################################################

def LABEL(parametros):     
    # Create the list of all the labels and their lines to be assigned in the jumps / branches
    labels.append([line.replace('.','').replace('\n','')]+[str(lineNumber)])
    #Replaces the labels into blankspace
    tok = re.sub('.*[A-Za-z0-9_-]',' ',line[0]) # <-- Regular expresion 

# Jump / Branch    
def JMP(i,parametros):
    # Searches for the line number and adds it to the final result (e.g. OPCode+0x00H ; H = line in code * 4 bits)
    for m in range(len(labels)):
        if parametros[1] == labels[m][0]:
            writetext("rom.txt", str(i)+". "+",".join(parametros), "0101"+space+("{:010b}".format(int(labels[m][1]))).zfill(28))
        else:
            continue

# Jump Greater Equal
def JGE(i,parametros):

    r_bin = []
    # Takes only items from position 1 and 2 of the list
    for n in range(len(parametros[1:-1])):
        r=formatbits.format(int(parametros[n+1][1:]))
        r_bin.append(r)
    values=space.join(r_bin)
    # Searches for the line number and adds it to the final result (e.g. OPCode+Rn+Rm+0x00H ; H = line in code * 4 bits)
    for m in range(len(labels)):
        if parametros[3] == labels[m][0]:
            comp_value = "0110"+space+values+space+("{:010b}".format(int(labels[m][1]))).zfill(16)
            writetext("rom.txt", str(i)+". "+",".join(parametros), comp_value) 
        else:
            continue

##############################################################################################
##################                  Register Functions                      ##################
##############################################################################################

def STORE(i,parametros):
    
    r_bin = []
    for n in range(len(parametros[1:])):
        r=formatbits.format(int(parametros[n+1][1:]))
        r_bin.append(r)
    values=space.join(r_bin)
    comp_line="1000"+space+values+space.zfill(16)
    writetext("rom.txt", str(i)+". "+",".join(parametros), comp_line) 

def LOAD(i,parametros): 

    r_bin = []
    for n in range(len(parametros[1:])):
        r=formatbits.format(int(parametros[n+1][1:]))
        r_bin.append(r)
    values=space.join(r_bin)
    comp_line="0111"+space+values+space.zfill(16)
    writetext("rom.txt", str(i)+". "+",".join(parametros), comp_line) 


#############################################################################################
##################                  Check for Instructions                 ##################
#############################################################################################

def instructionsSelection(parametros):
                       
        for i in range(len(tok)):
            instructionLine = tok[i][0]
            #Addition

            if instructionLine == "ADD":
                ADD(i+1,tok[i])
            #Substraction
            elif instructionLine == "SUB":
                SUB(i+1,tok[i])
            #Multiplication
            elif instructionLine == "MUL":
                MUL(i+1,tok[i])
            # Store
            elif instructionLine == "STR":
                STORE(i+1,tok[i])
            # Load
            elif instructionLine == "LD":
                LOAD(i+1,tok[i])
            # Jump / Branch    
            elif instructionLine == "JMP": 
                JMP(i+1,tok[i])
            # Jump Greater Equal
            elif instructionLine == "JGE":
                JGE(i+1,tok[i])
            #Invalid syntax
            else:
                print("Invalid register name")
                sys.exit()
            

#############################################################################################

fileName = input("Please enter the file name without the extension: ")
fileName = fileName + ".txt"
with open(fileName) as f:
    
    #reads the file per line
    for line in f:                    
        # Ignore comments   # Ignore blank spaces
        if line[0]=='#' or line[0]=='\n' or line[0]=='\r' or line[0]==' ' or line[0]=='   ':
            continue
        #Label
        elif line[0]=='.':
            LABEL(line)
            continue
        # Replace spaces          
        line = line.replace('\n', '').replace('\r', '').replace(',', '') 

        # Split the line on  space to create the list    
        pre_tok = re.split(r" ",line)

        if '' in pre_tok or ' ' in pre_tok:
            pre_tok.remove('').remove(' ')
        # Final list of clear instructions    
        tok.append(pre_tok)
        lineNumber+=1
    #call the selector with the list of instructions
    instructionsSelection(tok)
