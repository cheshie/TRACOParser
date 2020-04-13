from src import FileBuilder
from src import logger
from Parser.Parser import Parser
from Parser.Constructions import Constructions
from pprint import pprint
from argparse import ArgumentParser

def parse_arguments(args_parser = ArgumentParser(prog='PLUTO / TRACO Code Parser',
                                                 description='Parsing code from P/T to CUDA')):
    args_parser.add_argument('-i', '--infile', help='input file name', default='Examples/example1.c')
    args_parser.add_argument('-o', help='output file')

    return args_parser.parse_args()
#

def test_parser(parser=Parser(parse_arguments().infile)):
    print("RESULT OF PARSING: ")
    for x in parser.readfile().instructions:
        if isinstance(x, Constructions):
            pprint(dict(vars(x))['Constr'])
            if x.Constr.instructions:
                print("====inside for===")
                for ins in x.Constr.instructions:
                    if isinstance(ins, Constructions):
                        pprint(dict(vars(ins))['Constr'])
                    else:
                        print(ins)
                print("====end of for===")
        else:
            print(x)

test_parser()

# if __name__ == "__main__":
#     file_name = "Examples/example1.c"
#     # readfile() returns a dict('variables', 'instructions')
#     parsing_phrases = Parser(file_name).readfile()
#     filename = 'main'
#     FileBuilder(parsing_phrases, filename)
