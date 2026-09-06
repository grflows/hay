import sys
import os

NEWLINE = '\n'
QOUTES = 'QT'
KEYWORDS = {
    "print": 'PRNT'
}

def lexer(source):
    tokens = []
    length = len(source)
    i = 0

    while i < length:
        char = source[i] # we scan one char at a time

        if char in '\n':
            tokens.append('NL')
            i += 1
            continue

        if char.isspace(): 
            i += 1
            continue

        if char == "/": # skip comments till new line
            while i < length and source[i] != NEWLINE:
                i += 1
            tokens.append('CMNT')
            continue

        if char == '"':
            i += 1
            start = i
            while i < length and source[i] != '"':
                i += 1
            string = source[start:i]
            tokens.append(('STR', string))
            i += 1
            continue


        if 'a' < char < 'z':
            start = i
            while i < length and not source[i].isspace():
                i += 1
            word = source[start:i]
            tokens.append(KEYWORDS.get(word))
            continue
        i += 1

    return tokens


def parser(tokens):
    ast = []
    return ast



def main():
    if len(sys.argv) != 2:
        print("in correct usage. hay <file.hay>")
        exit()
    file_name = sys.argv[1]
    if os.path.exists(file_name):
        ext = os.path.splitext(file_name)[1]
        if ext == ".hay":
            with open(file_name, 'r') as f:
                source = f.read()

            tokens = lexer(source)
            ast = parser(tokens)
            print(ast)
        else:
            file_name = file_name.replace(ext, f"{ext}")
            print("incorrect file type. expected .hay")
    else:
        print("make sure the file path is correct")

main()
