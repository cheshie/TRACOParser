from Parser import Parser
from argparse import ArgumentParser
from pprint import pprint
from Constructions import Constructions

def parse_arguments(args_parser = ArgumentParser(prog='PLUTO / TRACO Code Parser',
                                                 description='Parsing code from P/T to CUDA')):
    args_parser.add_argument('-i', '--infile', help='input file name', default='../Examples/example2.c')
    args_parser.add_argument('-o', help='output file')

    return args_parser.parse_args()
#

def main():
    args = parse_arguments()
    parser = Parser(args.infile)
    parser.readfile()
    print("\n\nRESULT OF PARSING: ")
    for x in parser.file_structure.instructions:
        if isinstance(x, Constructions):
            pprint(dict(vars(x)))
            if x.Constr.instructions:
                print("====inside for===")
                for ins in x.Constr.instructions:
                    if isinstance(ins, Constructions):
                        pprint(dict(vars(ins)))
                    else:
                        print(ins)
                print("====end of for===")
        else:
            print(x)

# Just for testing
# if __name__ == "__main__":
#     main()