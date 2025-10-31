with open("input.txt","r") as file:
    code = file.read()
    print(code)

with open("basic functions.txt","r") as file:
    end_file = file.read()
    print(end_file)

compiled = []
variables = ["x"]

def c_a(a):
    compiled.append(a)

def print_(str_):
    i = 0
    char_ = ""
    if type(str_) == int and (str_ >=32768 or str_ <= -32769):
        print(">>> Keyerror: int out of bounds")
        return
    if not str_ in variables:
        for char in str_:
            i += 1
            if i%2==0:
                c_a("push r1")
                c_a("<U32>0b0010010000010000"+str(bin(ord(char)))+str(bin(ord(char_))))
                c_a("call printstr")
                c_a("pop r1")
            else:
                char_ = char
    else: 
        c_a("push r1")
        c_a("load_16 ["+str(variables.index(str_))+"],r1")
        c_a("call printint")
        c_a("pop r1")

print_("x")
