with open("input.txt","r") as file:
    code = file.read()
    print(code)

with open("basic functions.txt","r") as file:
    end_file = file.read()
    print(end_file)

compiled = []
variables = []

def c_a(a):
    compiled.append(a)


def print_(str_):
    i = 0
    char_ = ""
    if type(str_) == int and (str_ >=32768 or str_ <= -32769):
        print(">>> Keyerror: int out of bounds")
        return
    if not str_ in variables:
        c_a("push r1")
        for char in str_:
                c_a("<U32>0b001001000001000000000000"+str(bin(ord(char_))))
                c_a("store_8 [r12],r1")
        c_a("pop r1")
    else: 
        c_a("push r1")
        c_a("load_16 r1, ["+str(variables.index(str_))+"]")
        c_a("call printint")
        c_a("pop r1")

if_logic = {
    "==":"je",
    "!=":"jne",
    "<":"jg",
    ">":"jl",
    "<=":"jle",
    "=<":"jle",
    ">=":"jge",
    "=>":"jge"
    }

label_counter = 0

def if_(cond):
    num = 0
    varset = 0
    var = ""
    for char in cond:
        if char == "#": 
            break
        if char in "()=!<>":
            if char in "()":
                varset = 1  
#change wether we're using the character for a variable/number or a operand (if,in,and,or,not)
#otherwise we're using it in a comparator or variable
        if char in "0123456789":
            num *= 10
            num += int(char)
        elif char in "qwertyuiopasdfghjklzxcvbnm_":
            if varset == 0:
                var += char
print("hi")



import_turtle()





with open("compiled code.txt","w") as file:
    file.truncate(0) #clear the file
    for line in compiled:
        end_file += line + "\n"
    file.writelines(end_file)

