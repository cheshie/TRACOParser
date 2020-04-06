from collections import namedtuple, deque
from re import search, compile
import re
from Constructions import Constructions

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

