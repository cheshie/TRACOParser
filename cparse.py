from argparse import ArgumentParser
from collections import namedtuple, deque
from re import search, compile
import re


def parse_arguments(args_parser = ArgumentParser(prog='PLUTO / TRACO Code Parser',
                                                 description='Parsing code from P/T to CUDA')):
    args_parser.add_argument('-i', '--infile', help='input file name', default='example.c')
    args_parser.add_argument('-o', help='output file')

    return args_parser.parse_args()
#

class Constructions():
    def __init__(self, name):
        if name == 'for':                # tuple name cannot be known python keyword!
            self.Constr    = namedtuple('for_n', ['init', 'end_condition', 'increment', 'instruction', 'original_line']) # last parameter is just a string representing orig. line
                                                                            # TODO: parallel for's should be special-marked!
            # TODO: Special case: what if incrementation is outside???
            self.method    = self.eval_for
        if name =='pragma':
            self.Constr    =  namedtuple('pragma', ['text', 'instruction'])
            self.method    = self.eval_pragma
        if name =='variable':
            self.Constr = namedtuple('var', ['name', 'value', 'size', 'type'])
    #
    # {} <= in the future, how to recognize it
    def eval_for(self, instruction):
        # TODO: For special cases - not handled yet!
        self.Constr.init, self.Constr.end_condition, self.Constr.increment = \
            search(r'.*?\((.*)\).*', instruction).group(1).split(';')
        # i = n; i >= 0; i--
        # i = 0; i <= n; i++
        # Case 1: for (init ; end_condition ; increment ) => handled ONLY THIS CASE IS INTERESTING
        # Always will be i++, never ++i
        # Case 2: for ( ; ; ) => not handled
        # Case 3: for (init; end_condition; ) => not handled
        # Case 4: for (;end_condition; increment) => not handled
        # Case 5: for (;; increment) => not handled
        #                ^ are these semicolons needed?
        # Case 6: (special) i.e. for ( int i, j; i < 5,j>3; i++,j++ )
    #

    def eval_pragma(self, instruction):
        pass
        #self.Constr.text = instruction
    #
#

class Parser():
    def __init__(self, input):
        self.in_fname   = input #CHANGE THIS NAME - python keyword
        self.f_contents = None
        self.file_structure = {'include': None, 'variables': None, 'instructions' : []}
        self.keywords       = {'for', 'pragma'}
    #

    def readfile(self):
        with open(self.in_fname, 'r') as lines:
            # Read contents of the file
            self.f_contents = deque(list(lines)[1:]) # LEAVE 1st LINE (pragma) for now!
            for line in self.f_contents:
                # If empty line spotted, skip a line
                if search(r'^$', line):
                    continue

                # Read first word in line, prepended by # or not
                instruction = search(r'^(\s*)[#]{0,1}(\w+)', line).group(1)

                # Check if its in keywords
                if instruction in self.keywords:
                    # Create object containing code in the line
                    ins_struct = Constructions(instruction)
                    self.file_structure['instructions'] = ins_struct #list of instructions
                    self.file_structure['instructions'].method(line.replace(instruction, ''))
                else:
                    # Assign variable here
                    pass
    #

    # To print class into a readable format
    def __str__(self):
        # ALL VARIABLES AND INSTRUCTIONS IN JSON FORMAT HER???
        return "pass"
#

if __name__ == '__main__':
    args = parse_arguments()
    parser = Parser(args.infile)
    parser.readfile()
