from collections import namedtuple, deque
from re import search, compile
import re

class Constructions():
    def __init__(self, name):
        if name == 'for':
            self.method    = self.eval_for
        if name =='pragma':
            self.Constr    =  namedtuple('pragma', ['text', 'instruction'])
            self.method    = self.eval_pragma
        if name =='variable':
            self.Constr = namedtuple('var', ['name', 'value', 'size', 'type'])

    def eval_for(self, instruction, variables, is_parallel=False):
        # Case 1: for (init ; end_condition ; increment ) => handled (and only this is interesting)
        # Prototype of construction namedtuple
        For = namedtuple('for_n', ['init', 'end_condition', 'increment', 'instructions','variables', 'is_parallel', 'original_line'])

        # Split into three groups: group1; group2; group3
        txt_init, txt_cond, txt_inc     = search(r'.*?\((.*)\).*', instruction).group(1).split(';')
        # Evaluate groups
        init_var, init_equal, init_val  = search(r'\s?((\w+)\s?(=)\s?(\w+))', txt_init).group(2, 3, 4)
        cond_var, cond_sign, cond_val = search(r'\s?((\w+)\s?(==|>=|<=|<|>)\s?(\w+))', txt_cond).group(2,3,4)
        inc_var,  inc_sign,  inc_val      = search(r'\s?((\w+)\s?(\+\+|--|\+=|-=)\s?(\w*))', txt_inc).group(2,3,4)

        # Evaluate group 2 - end condition
        # Case 1: i <= n
        # If there is no = sign, means that end_condition value must be decremented
        # So that the value it contains is the last value that i takes in this loop
        # Case 2: i >= n
        # If i variable is decrementing each step of the loop, and there is =
        # sign, last value it takes is equal to n. Otherwise, n + 1
        # # # # # # # # # # #
        # var   - variable that is tested in condition
        # value - last value that this variable must take in order to exit condition
        end_cond_dict = {'var': cond_var, 'value': None}

        # Check whether accessed variable has been initialized
        if cond_val not in variables:
            # For now we just raise the Exception, but it should be our own class here
            raise Exception(f'[!] Variable {cond_val} has not been declared')

        # Case 1:
        if '+' in inc_sign:
            if '=' in cond_sign:
                end_cond_dict['value'] = cond_val
            else:
                end_cond_dict['value'] = cond_val + '- 1'
        # Case 2:
        else:
            if '=' in cond_sign:
                end_cond_dict['value'] = cond_val
            else:
                end_cond_dict['value'] = cond_val + '- 1'

        # Evaluate group 3 - incrementation
        # # # # # # # #
        # var - variable that is being inc/decremented
        # inc - value that is used to increment i.e.
        # 1  => means ++
        # -1 => means --
        # 2  => means += 2
        # -3 => means -= 3
        inc_dict = {'var' : inc_var, 'inc' : None}
        if inc_val == '':
            if '++' in inc_sign:
                inc_dict['inc'] = 1
            elif '--' in inc_sign:
                inc_dict['inc'] = -1
        else:
            # The += case:
            if '+' in inc_sign:
                inc_dict['inc'] = int(inc_val)
            # The -= case:
            elif '-' in inc_sign:
                inc_dict['inc'] = (-1) * int(inc_val)

        self.Constr = For(init={'name': init_var, 'value': int(init_val)},
                          end_condition=end_cond_dict,
                          increment=inc_dict,
                          instructions= [],
                          original_line= instruction,
                          is_parallel  = is_parallel,
                          variables =dict())
    #

    def eval_pragma(self, instruction):
        pass
    #
#
