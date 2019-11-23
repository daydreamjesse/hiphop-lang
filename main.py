from hiphopparse import Parser
from termcolor import colored
import sys 

def print_help():
    docs = [
        "open <filename> as <id>:",
        "   opens an image at the given filename, saving it as id within the program\n",
        "save <id> as <filename>:",
        "   saves image saved as id within the program to the given filename\n",
        "apply <func> to <id>:",
        "   applies the given function or saved macro to image saved at id\n",
        "apply-all [<funcs>] to <id>:",
        "   applies a chain of functions to the image saved at id\n",
        "save-macro [<funcs>] as <id>:",
        "   saves a chain of functions to the given id to be invoked later\n"
    ]
    for line in docs:
        print(colored(line, "blue"))
    print(colored("For a list of built in image processing functions, type `list functions`", "red"))

def print_functions():
    functions = [
        "scale x y",
        "blur radius",
        "grayscale",
        "erode radius",
        "dilate radius",
        "outline radius",
        "filtercolor lowR lowG lowB highR highG highB",
        "crop widthlow widthhigh heightlow heighthigh",
    ]
    for line in functions:
        print(colored(line, "blue"))

def main():

    parser = Parser()
    
    # count number of arguments
    if (len(sys.argv) == 2):
        filename = sys.argv[1]
        print("Interpreting HIPHOP program with the filename: {}".format(filename))
        parser.parse(filename)
    if (len(sys.argv) == 1):
        print(colored("Starting HIPHOP command line program...", "cyan"))
        print(colored("Type `q` or `quit` to exit. `h` or `help` for functions.", "red"))
        while (True):
            line = input(colored("hee hee >>> ", "cyan"))
            if (line.strip() == "quit" or line.strip() == "q"):
                break
            if (line.strip() == "h" or line.strip() == "help"):
                print_help()
            if (line.strip() == "list functions"):
                print_functions()
            parser.parse_line(line)
        print(colored("Quitting HIPHOP command line.", "cyan"))
    else:
        print("Usage: `python main.py <filename>` or `python main.py`")

if __name__ == "__main__":
    main()