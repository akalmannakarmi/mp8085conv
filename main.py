# Program to convert 8085 instruction to hex code

# Imports
import json

# Global vars
ins1Byte = {}
ins2Byte = {}
ins3Byte = {}
insJump = {}
labels = {}
codes = []
result = {}
currentAddr = 0xC000    #Starting address

def loadInstructions():     #Loads all the instructions to Dictionary
    global ins1Byte,ins2Byte,ins3Byte,insJump
    with open("D:\Documents\IT-Club-Class\projects\project1/1byte.json") as file:
        ins1Byte = json.load(file)
    with open("D:\Documents\IT-Club-Class\projects\project1/2byte.json") as file:
        ins2Byte = json.load(file)
    with open("D:\Documents\IT-Club-Class\projects\project1/3byte.json") as file:
        ins3Byte = json.load(file)
    with open("D:\Documents\IT-Club-Class\projects\project1/jump.json") as file:
        insJump = json.load(file)
        
def readCode(): #Reads the code file and stores in codes
    global codes
    with open("D:\Documents\IT-Club-Class\projects\project1/code.txt") as file:
        codes = file.readlines()
        
def writeResult():  #Writes the result to result.txt
    global result
    with open("D:\Documents\IT-Club-Class\projects\project1/result.txt","w") as file:
        for address,data in result.items():
            file.writelines(f"{hex(address)[2:].upper()} {data}\n")
        
def addDatas(datas):    #Adds the data to the address
    global result,currentAddr
    for data in datas:
        result[currentAddr] = data
        currentAddr +=0x1
        
def convert(code):  #Convers the given instruction to hex code
    global codes,ins1Byte,ins2Byte,ins3Byte,insJump,labels,result
    datas = []
    for instruction in ins1Byte:
        if code.find(instruction)!=-1:
            datas.append(ins1Byte[instruction])
            return datas
    for instruction in ins2Byte:
        if code.find(instruction)!=-1:
            datas.append(ins2Byte[instruction])
            data = code.replace(instruction,"").strip()
            datas.append(data)
            return datas
    for instruction in ins3Byte:
        if code.find(instruction)!=-1:
            datas.append(ins3Byte[instruction])
            data = code.replace(instruction,"").strip()
            datas.append(data[2:4])
            datas.append(data[:2])
            return datas
    for instruction in insJump:
        if code.find(instruction)!=-1:
            datas.append(insJump[instruction])
            label =code.replace(instruction,"").strip()
            datas.append(label)
            datas.append("")
            return datas

def convertCode():  #Converts the code to hex values
    global codes,labels,result,currentAddr
    for code in codes:
        if code.find(":") !=-1:
            labels[code.split(":")[0]]=currentAddr
            code = code.split(":")[1]
        datas = convert(code)
        addDatas(datas)
    placeLabels()
    
def placeLabels():  #Replace the placeholder address names with actuall address
    global result,labels
    for address,data in result.items():
        for label in labels:
            if data == label:
                result[address] = hex(labels[label])[4:6].upper()
                result[address+0x1] = hex(labels[label])[2:4].upper()

# Extra code
def printInstructions():    #Prints all the loaded Instructions 
    print(f"1 Byte instructions")
    print(f"Opcodes\tHex Code")
    for opcode,hexCode in ins1Byte.items():
        print(f"{opcode}\t{hexCode}")
    print(f"2 Byte instructions")
    print(f"Opcodes\tHex Code")
    for opcode,hexCode in ins2Byte.items():
        print(f"{opcode}\t{hexCode}")
    print(f"3 Byte instructions")
    print(f"Opcodes\tHex Code")
    for opcode,hexCode in ins3Byte.items():
        print(f"{opcode}\t{hexCode}")
    print(f"Jump instructions")
    print(f"Opcodes\tHex Code")
    for opcode,hexCode in insJump.items():
        print(f"{opcode}\t{hexCode}")

#Extra code
def printCodeNResult(): #Prints The result 
    global codes,result
    print("-------------\nCode")
    for code in codes:
        print(code.strip())
    print("-------------\nResult:")
    for address,data in result.items():
        print(hex(address)[2:].upper(),data)


def run():
    loadInstructions()
    # printInstructions()
    
    readCode()
    convertCode()
    
    writeResult()
    printCodeNResult()
    

    
if __name__ == "__main__":
    run()