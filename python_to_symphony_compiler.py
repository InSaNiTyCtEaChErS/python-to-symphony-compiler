with open("input.txt","r") as file: #load input
    code = file.read()
    print(code)

with open("basic functions.txt","r") as file: #load basic functions
    end_file = file.read()
    print(end_file)

compiled = []
variables = []

def c_a(a):
    compiled.append(a)
line = 0

def calc(expressions):
    
    precedence = {'+': 1, '-': 1, '<<': 1,'>>': 1, '*': 2, '/': 2, '^': 3}
    output = []
    output2 = []
    operator_stack = []
    expression = ""
    i = 0


    for character in expressions:
        expression += character
        if character != " ":
            expression += " "

    tokens = expression.split()

    for token in tokens:
        i += 1
        print("token = "+token)
        if i >= 13:
            raise ValueError(f"line: {line} too many tokens in expression: {expression}")

        if token == "=":
            output.append(output[0])
        elif token in variables:
            c_a("load_16 r"+str(i)+" ["+str(variables.index(token)*4)+"]") #handle variables
            output.append("r"+str(i))
        elif token.isnumeric() or (token.startswith('-') and token[1:].isnumeric()):  # Handle numbers (including negative)
            c_a("mov r"+str(i)+" "+str(token))
            output.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Pop the '('
        elif token in precedence:
            while (operator_stack and operator_stack[-1] != '(' and
                    precedence.get(operator_stack[-1], 0) >= precedence[token]):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            raise ValueError(f"Invalid token: {token}")

    c_a("mov r"+str(i)+",r13")
    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Mismatched parentheses in expression")
        output.append(operator_stack.pop())

    return " ".join(output2)+' '.join(output) #returns RPN of the inputted expression or expressionlet

def setvar(line):
    
    index = line.find("=")
    variables += (line[0:index-1])
    temp = variables.find(line[0:index-1])
    c_a("load_16 r1, ["+temp+"]")

    calc(line)

    c_a("store_16 ["+temp+"]")
        


def print_(str_):
    str_ = str_.strip('"').strip("'")
    i = 0
    char_ = ""
    if type(str_) == int and (str_ >=32768 or str_ <= -32769):
        print(">>> Keyerror: int out of bounds")
        return
    if not str_ in variables:
        for char in str_:
                c_a("<U32>0b001001000001000000000000"+str(bin(ord(char_))))
                c_a("store_8 [r12],r1")
    else: 
        c_a("load_16 r1, ["+str(variables.index(str_))+"]")
        c_a("call printint")

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

for line in code:
    if "#" in line:
        line=line[0:line.find("#")] #remove comments, ex: this one

    if "if" in line or "elif" in line: #if/elif
        if_(line)
    elif "print" in line: #print
        print_(line)
    elif "for" in line: #loops
        print("ADD LOOPS -- for")
    elif "while" in line:
        print("ADD LOOPS-- while")
    elif "def" in line: #functions
        print("ADD DEFINING")
    else:
        setvar(line)

#write resultant code
with open("compiled code.txt","w") as file:
    file.truncate(0) #clear the file
    for line in compiled:
        end_file += line + "\n"
    file.writelines(end_file)

