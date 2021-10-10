##############################################################################################
'''
Compiler for custom assembly ISA

The program creates a text file with the hexadecimal values of the instructions
to be uploaded to the processor (CPU) 

Inputs --> text file with the instructions following the nomenclature
Outputs --> rom.txt file with hexadecimal equivalent of the instructions

'''
##############################################################################################

import sys
import re
import csv

##############################################################################################
##################                  Variables                               ##################
##############################################################################################

bits = 8
formatbits = "{:#08}"
labels = []
lineNumber=1
tok = []

##############################################################################################

def writetext(fn, b):
    #Output file
	with open("rom.txt", "a") as new_file:
        	new_file.write(str(b)+" ")

##############################################################################################
##################                  Arithmetic Functions                    ##################
##############################################################################################

#Addition
def ADD(parametros): 

    r_hexa = []
    for n in range(len(parametros[1:-1])):
        r=formatbits.format(int(parametros[n+1][1:]),6)
        r_hexa.append(r)
    values=''.join(r_hexa)
    # Case ADD Rn, Rm, Rl
    if parametros[3][0] == "R":
        comp_line="42".zfill(bits)+values+str(parametros[3][1:]).zfill(bits)
        writetext("rom.txt", comp_line) 
    else:
    # Case ADD Rn, Rm, l         
        comp_line="43".zfill(bits)+values+(str(parametros[3])).zfill(bits)
        writetext("rom.txt", comp_line)    
#Substraction
def SUB(parametros):

    r_hexa = []
    for n in range(len(parametros[1:-1])):
        r=formatbits.format(int(parametros[n+1][1:]),6)
        r_hexa.append(r)
    values=''.join(r_hexa)
    # Case SUB Rn, Rm, Rl
    if parametros[3][0] == "R":
        comp_line="44".zfill(bits)+values+str(parametros[3][1:]).zfill(bits)
        writetext("rom.txt", comp_line) 
    else:
    # Case SUB Rn, Rm, l         
        comp_line="45".zfill(bits)+values+(str(parametros[3])).zfill(bits)
        writetext("rom.txt", comp_line)          

#Multiplication
def MUL(parametros): 
      
    r_hexa = []
    for n in range(len(parametros[1:-1])):
        r=formatbits.format(int(parametros[n+1][1:]),6)
        r_hexa.append(r)
    values=''.join(r_hexa)
    # Case MUL Rn, Rm, Rl
    if parametros[3][0] == "R":
        comp_line="46".zfill(bits)+values+str(parametros[3][1:]).zfill(bits)
        writetext("rom.txt", comp_line) 
    else:
    # Case MUL Rn, Rm, l         
        comp_line="47".zfill(bits)+values+(str(parametros[3])).zfill(bits)
        writetext("rom.txt", comp_line)  
 
##############################################################################################
##################                  Conditional Functions                    ##################
##############################################################################################

def LABEL(parametros):     
    # Create the list of all the labels and their lines to be asigned in the jumps / branches
    labels.append([line.replace('.','').replace('\n','')]+[str(lineNumber)])
    #Replaces the labels into blankspace
    tok = re.sub('.*[A-Za-z0-9_-]',' ',line[0]) # <-- Regular expresion 

# Jump / Branch    
def JMP(parametros):
    # Searches for the line number and adds it to the final result (e.g. OPCode+0x00H ; H = line in code * 4 bits)
    for m in range(len(labels)):
        if parametros[1] == labels[m][0]:
            writetext("rom.txt", "48".zfill(bits)+str(labels[m][1]).zfill(bits))
        else:
            continue

# Jump Greater Equal
def JGE(parametros):

    r_hexa = []
    # Takes only items from position 1 and 2 of the list
    for n in range(len(parametros[1:-1])):
        r=formatbits.format(int(parametros[n+1][1:]),6)
        r_hexa.append(r)
    values=''.join(r_hexa)
    # Searches for the line number and adds it to the final result (e.g. OPCode+Rn+Rm+0x00H ; H = line in code * 4 bits)
    for m in range(len(labels)):
        if parametros[3] == labels[m][0]:
            comp_value = "49".zfill(bits)+values+str(labels[m][1]).zfill(bits)
            writetext("rom.txt", comp_value)
        else:
            continue

##############################################################################################
##################                  Register Functions                      ##################
##############################################################################################

def STORE(parametros):
    
    r_hexa = []
    r=formatbits.format(int(parametros[1][1:]),6)
    # Case STR Rn, Rm
    if parametros[1][0] == "R":
        comp_line="50".zfill(bits)+r+str(parametros[2][1:]).zfill(bits)
        writetext("rom.txt", comp_line) 
    else:
    # Case STR Rn, m        
        comp_line="51".zfill(bits)+r+(str(parametros[2])).zfill(bits)
        writetext("rom.txt", comp_line) 

def LOAD(parametros): 

    r_hexa = []
    r=formatbits.format(int(parametros[1][1:]),6)
    # Case LD Rn, Rm
    if parametros[1][0] == "R":
        comp_line="52".zfill(bits)+r+str(parametros[2][1:]).zfill(bits)
        writetext("rom.txt", comp_line) 
    else:
    # Case LD Rn, m        
        comp_line="53".zfill(bits)+r+(str(parametros[2])).zfill(bits)
        writetext("rom.txt", comp_line) 

def MOVE(parametros): 

    r_hexa = []
    r=formatbits.format(int(parametros[1][1:]),6)
    # Case MOV Rn, Rm
    if parametros[1][0] == "R":
        comp_line="54".zfill(bits)+r+str(parametros[2][1:]).zfill(bits)
        writetext("rom.txt", comp_line) 
    else:
    # Case MOV Rn, m        
        comp_line="55".zfill(bits)+r+(str(parametros[2])).zfill(bits)
        writetext("rom.txt", comp_line) 

#############################################################################################
##################                  Check for Instructions                 ##################
#############################################################################################

def instructionsSelection(parametros):
                       
        for i in range(len(tok)):
            instruction = tok[i][0]
            #Addition
            if instruction == "ADD":
                ADD(tok[i])
            #Substraction
            elif instruction == "SUB":
                SUB(tok[i])
            #Multiplication
            elif instruction == "MUL":
                MUL(tok[i])
            # Store
            elif instruction == "STR":
                STORE(tok[i])
            # Load
            elif instruction == "LD":
                LOAD(tok[i])
            # Move
            elif instruction == "MV":
                MOVE(tok[i])
            # Jump / Branch    
            elif instruction == "JMP": 
                JMP(tok[i])
            # Jump Greater Equal
            elif instruction == "JGE":
                JGE(tok[i])
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

                
 




'''    a1 = tok[2]   
    r_hexa = []

    for x in range(len(tok[1:])):
        #r="{0:#0{1}x}".format(int(tok[x+1].upper()[1]),6)
        r=formatbits.format(int(tok[x+1].upper()[1]))
        r_hexa.append(r)
    values=''.join(r_hexa)    
    #Register  (ADD Rn, Rm, Ro)
    if a1[0] == 'R':
        comp_line="42".zfill(bits)+values
        writetext("rom.txt", comp_line)
    #Value  (ADD Rn, m)
    else:
        comp_line="43".zfill(bits)+values
        writetext("rom.txt", comp_line)'''

                    

    



