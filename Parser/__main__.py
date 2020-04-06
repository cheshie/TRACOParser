from Parser import Parser
from argparse import ArgumentParser

def parse_arguments(args_parser = ArgumentParser(prog='PLUTO / TRACO Code Parser',
                                                 description='Parsing code from P/T to CUDA')):
    args_parser.add_argument('-i', '--infile', help='input file name', default='../Examples/example.c')
    args_parser.add_argument('-o', help='output file')

    return args_parser.parse_args()
#

def main():
    args = parse_arguments()
    parser = Parser(args.infile)
    parser.readfile()

# Just for testing
if __name__ == "__main__":
    main()