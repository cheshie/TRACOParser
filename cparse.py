from argparse import ArgumentParser
from _collections import namedtuple

# Parse command line arguments
def parse_arguments(args_parser = ArgumentParser(prog='PLUTO / TRACO Code Parser',
                                                 description='Parsing code from P/T to CUDA')):
    args_parser.add_argument('-i', '--infile', help='input file name', default='example.c')
    args_parser.add_argument('-o', help='output file')

    # Return parsed arguments and a list containing dictionaries for separate groups
    return args_parser.parse_args()
#

class Parser():
    def __init__(self, input):
        self.in_fname   = input
        self.f_contents = None
    #

    def readfile(self):
        with open(self.in_fname, 'r') as lines:
            self.f_contents = lines
            for x in self.f_contents:
                print(x)
    #

    # Which on of this methods is used to print etc?
    def __str__(self):
        return "what"
#

if __name__ == '__main__':
    args = parse_arguments()
    parser = Parser(args.infile)
    parser.readfile()
