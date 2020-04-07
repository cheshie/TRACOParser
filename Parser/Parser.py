from collections import namedtuple, deque
from re import search, compile
import re
from .Constructions import Constructions

class Parser():
    def __init__(self, inpt):
        self.in_fname   = inpt
        self.f_contents = None
        # Namedtuple that contains info about program - initialized variables, executed instructions
        File = namedtuple('File_struct', ['variables', 'instructions'])
        self.file_structure = File(variables=dict(), instructions=[])
        # Available keywords
        self.keywords       = {'for', 'pragma'}
        # Counter holds info about which line (- 1) is currently processed
        self.instr_nr = 0
    #

    def readfile(self):
        with open(self.in_fname, 'r') as lines:
            # Read contents of the file
            self.f_contents = deque(lines) # LEAVE 1st LINE (pragma) for now!
            # This deque will just hold dicts with keys:
            # line         => nr of line where for started
            # is_multiline => if '{' spotted, mark this for as multiline
            # addr         => address to Construction that holds information about current for
            # It will works as a stack, each time we spot for, we push it here
            # Each time we spot '{', we mark current for as multiline
            # If is_multiline is set (True), pop current for from deque after spotting '}'
            # If its not multiline, just pop it after moving one instruction
            inside_for   = deque()

            # How many instructions after keyword "pragma" should be marked as parallel:
            pragma_depth = 1 # Pragma only for 1st for
            # Just to indicate for that particular instruction whether to mark it or not
            is_parallel  = False

            # For now, just declare hardcoded N variable, but this must change!
            self.file_structure.variables['N'] = 5
            self.file_structure.variables['A'] = {'name' : 'A', 'size' : (5, 5)}

            for line in self.f_contents:
                # Remove all trailing and leading whitespaces
                line = line.strip()

                # If empty line spotted, skip a line
                if search(r'^$', line):
                    continue

                # Handle multiline 'for' opening
                if line == '{':
                    inside_for[-1]['is_multiline'] = True
                    self.instr_nr += 1
                    continue
                # Handle multiline 'for' closing
                if line == '}':
                    inside_for.pop()
                    self.instr_nr += 1
                    continue

                # Read first word in line, prepended by # or not
                instruction = search(r'^(\s*)([#]{0,1})(\s*)(\w+)', line).group(2,3,4)[-1]

                if inside_for:
                    # If its a single-line for (w/o '{}'), then pop it
                    if inside_for[-1]['is_multiline'] is False and self.instr_nr - inside_for[-1]['line'] > 1:
                        print("Popping")
                        inside_for.pop()

                # Check if its in keywords
                if instruction in self.keywords:
                    if instruction == 'pragma':
                        is_parallel = True
                        self.file_structure.instructions.append('pragma')
                        # Move to the next instruction in source file
                        self.instr_nr += 1
                        continue

                    # Create object containing code in the line
                    ins_struct = Constructions(instruction)
                    ins_struct.method(line, self.file_structure.variables, is_parallel)

                    # instruction should be nested in a for
                    if inside_for:
                        # If inside_for contains information about any for, assign next instruction
                        # To that for's list of instructions
                        # inside_for[-1]['addr'] = ins_struct
                        inside_for[-1]['addr'].Constr.instructions.append(ins_struct) # inside_for[-1]['line']
                        # Add address to the structure so that it will be easier accessible from nested for/fors
                    # Check if deque is empty - meaning this instruction is not inside any for
                    else:
                        self.file_structure.instructions.append(ins_struct)

                    # Evaluate pragma depth. If it reached zero, just stop marking next for as parallel
                    if is_parallel:
                        pragma_depth -= 1
                        if pragma_depth == 0:
                            is_parallel = False

                    if instruction == 'for':
                        inside_for.append({'line' : self.instr_nr, 'is_multiline' : False, 'addr' : ins_struct})

                    print("Current for: ", inside_for)

                # Current instruction is not in keywords
                # Meaning its i.e. variable operation
                else:
                    # All lines must be terminated
                    if line.endswith(';'):
                        # Split line into variable thas is assigned to, index and value that is asssigned
                        var, index, val = search(r'^(\s*)(\w+)((\[\w+\])*)(\s*)(=)(\s*)(\w+)(;)', line).group(2,3,8)

                        # If variable does not exist
                        if var not in self.file_structure.variables:
                            # For now we just raise the Exception, but it should be our own class here
                            raise Exception(f'[!] Variable {var} has not been declared')

                        # Store info about variable assignment
                        # var   => variable name, must be an existing variable
                        # index => if empty, assign to a variable. Otherwise, assign to a list, so it will contain full index for example. [i] or [i][j]
                        # val   => value to assign
                        # original_line => just for reference
                        assign_dict = {'var' : var, 'index' : 0 if index == '' else index, 'val' : val, 'original_line' : line}

                        if inside_for:
                            # If inside_for contains information about any for, assign next instruction
                            # To that for's list of instructions
                            print("last for: ", inside_for[-1])
                            inside_for[-1]['addr'].Constr.instructions.append(
                                assign_dict)
                        else:
                            self.file_structure.instructions.append(assign_dict)
                    else:
                        raise Exception("[!] Lines should be terminated with ';'")

                # Move to the next instruction in source file
                self.instr_nr += 1
    #

    # To print class into a readable format
    def __str__(self):
        # ALL VARIABLES AND INSTRUCTIONS IN JSON FORMAT HER???
        return "pass"
#

