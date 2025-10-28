with open("input.txt","r") as file:
    code = file.read()
    print(code)

with open("basic functions.txt","r") as file:
    compiled = file.readlines
    print(compiled)
variables = []

def print_(str_):
    i = 0
    char_ = ""
    if not str_ in variables:
        for char in str_:
            i += 1
            if i%2==0:
                compiled.append("<U32>0b0010010000010000"+str(bin(ord(char)))+str(bin(ord(char_))))
            else:
                char_ = char

