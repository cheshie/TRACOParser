from collections import namedtuple, deque
from re import search, compile
import re

class Constructions():
    def __init__(self, name):
        if name == 'for':                # tuple name cannot be known python keyword!
                                         # {'name' : 'i', 'value': 0}       i.e. -1 or 1
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