import sys
import os

def lexer(file_name):
    return "lexed"





def main():
    if len(sys.argv) != 2:
        print("in correct usage. hay <file.hay>")
        exit()
    file_name = sys.argv[1]
    if os.path.exists(file_name):
        ext = os.path.splitext(file_name)[1]
        if ext == ".hay":
            tokens = lexer(file_name)
            print(tokens)
        else:
            file_name = file_name.replace(ext, f"{ext}")
            print("incorrect file type. expected .hay")
    else:
        print("make sure the file path is correct")

main()
