import os
import logging
import json
from typing import TextIO

from Parser.Constructions import Constructions

logger = logging.getLogger(__name__)

N = 5
r1 = N
c1 = N
c2 = N
_ext = '.cu'

lib_folder = os.getcwd() + '/libs'
if not os.path.exists(lib_folder):
    os.makedirs(lib_folder)
prod_folder = os.getcwd() + '/Products'
if not os.path.exists(prod_folder):
    os.makedirs(prod_folder)

constFiles = {
    0: 'LIBRARIES',
    1: 'NAMESPACES',
    2: 'KEYWORDS',
    3: 'FUNCTIONS',
    4: 'TYPESVARIABLES',
    5: 'VARIABLES',
    6: 'VALUES'
}
resources = {}

for i in constFiles.values():
    with open('{0}/{1}.txt'.format(lib_folder, i.lower()), 'r') as f:
        resources[i] = f.read().splitlines()

libraries = resources[constFiles[0]]
namespaces = resources[constFiles[1]]
keyWords = resources[constFiles[2]]
functions = resources[constFiles[3]]
typesVariables = resources[constFiles[4]]
variables = resources[constFiles[5]]
values = resources[constFiles[6]]


class FileBuilder:
    file: TextIO

    def __init__(self, phrase, filename):
        logger.info('Initialized FileBuilder')
        self.phrase = phrase
        self.make_file(filename)

    def make_file(self, filename):
        self.file = open(
            '{0}/{1}{2}'.format(prod_folder, filename, _ext), 'w+')
        self.building_file()
        self.file.close()
        logger.info('Created file')

    def check_variables_type(self):
        logger.info("Checking the type of variables")
        if self.phrase.variables:
            for var in self.phrase.variables:
                if type(self.phrase.variables[var]) is not dict:
                    logger.warning('var: {} is {} '.format(
                        var, type(self.phrase.variables[var]), ))
                if type(self.phrase.variables[var]) is dict:
                    logger.warning('{} is matrix'.format(var))
        else:
            logger.warning('no variables')

    # file.phrase.instructions[1].Constr.instructions[0].Constr.instructions[0]
    @staticmethod
    def check_variables_type2(variables):
        logger.info("Checking the type of variables with strange method")
        if variables:
            for var in variables:
                if type(variables[var]) is not dict:
                    logger.warning('var: {} is {} type --> {}'.format(
                        var, type(variables[var]), variables[var]))
                if type(variables[var]) is dict:
                    logger.warning('{} is matrix'.format(var))

    # building_for - function to create loop for
    # variable - loop's variable
    # condition - condition's variable
    # start - init value
    # step - step in loop
    # stop - end value
    # inside - loop body
    @staticmethod
    def building_for(variable, condition, start, step, stop, inside=''):
        logger.info("Building for")
        return f"for(int {variable} = {start}; {variable} {condition} {stop}; {variable} = {variable} + {step})\n{{ \n\t{inside} }}"

    # declaration_variable_with_value - function to create variable with value
    # type - variable type
    # name - variable name
    # value - init value
    @staticmethod
    def declaration_variable_with_value(type, name, value):
        logger.info("Building var with val")
        return f"{type} {name} = {value}"

    # declaration_variable - function to create variable
    # type - variable type
    # name - variable name
    @staticmethod
    def declaration_variable(type, name):
        logger.info("Building var without val")
        return f"{type} {name}"

    # creating_function - function to create function
    # returnType - return variable type
    # name - function name
    # typedef - definition typedef
    # param - parameters taken by the function
    @staticmethod
    def creating_function(returnType, name, typedef='', param=''):
        logger.info("Building func")
        return f"{typedef} {returnType} {name}({param}) {{ "

    # creating_two_dimensional_array - function to create two dimensional array
    # type - array type
    # name - array name
    # first_dim - first dimension of the array
    # second_dim - second dimension of the array
    @staticmethod
    def creating_two_dimensional_array(type, name, first_dim, second_dim):
        logger.info("Building array two dim")
        return f"{type} {name}[{first_dim}][{second_dim}]"

    # creating_one_dimensional_array - function to create array
    # type - array type
    # name - array name
    # first_dim - first dimension of the array
    # typedef - definition typedef
    @staticmethod
    def creating_one_dimensional_array(type, name, first_dim, typedef=''):
        logger.info("Building array one dim")
        return f"{typedef} {type} {name}[{first_dim}]"

    # lt_or_gt - function for determining the sign "less than" or "greater than"
    # type - variable type
    # name - variable name
    @staticmethod
    def lt_or_gt(startValue, endValue):
        if startValue < endValue:
            return '<'
        else:
            return '>'

    def building_main(self):
        # TODO: build main body -> loops, variables, etc.
        # int main() {
        self.file.writelines(
            "\n\n" + self.creating_function(typesVariables[0], functions[1], '', '') + "\n")

        # int rows = N;
        # int cols = N;
        # arrtype *dA;
        self.file.writelines("\t" + self.declaration_variable_with_value(
            typesVariables[0], variables[11], variables[0]) + ";\n")
        self.file.writelines("\t" + self.declaration_variable_with_value(
            typesVariables[0], variables[12], variables[0]) + ";\n")
        self.file.writelines(
            "\t" + self.declaration_variable(variables[1], '*dA') + ";\n")

        # int** A = new int*[rows];
        self.file.writelines("\t" + self.declaration_variable_with_value(
            typesVariables[2], variables[14],
            self.creating_one_dimensional_array('new', typesVariables[1], variables[11])) + ";\n")

        # A[0] = new int[rows * cols];
        self.file.writelines("  " + self.creating_one_dimensional_array(
            '', variables[14], 0) + "=" + self.creating_one_dimensional_array('new', typesVariables[0],
                                                                              'rows*cols') + ";\n")


        # for (int i = 1; i < rows; ++i) { A[i] = A[i-1] + cols; };
        self.file.writelines("\n\t" + self.building_for('int i', self.lt_or_gt(1, 10), 1, 1, variables[11],
                                                        self.creating_one_dimensional_array(
                                                            '', variables[14],
                                                            'i') + "=" + self.creating_one_dimensional_array('',
                                                                                                           variables[
                                                                                                               14],
                                                                                                           'i-1') + " + cols;\n\t") + "\n")

        for instr in self.phrase.instructions:
            if isinstance(instr, Constructions):
                for instr2 in instr.Constr.instructions:
                    if isinstance(instr2, Constructions):
                        for instr3 in instr2.Constr.instructions:
                            if isinstance(instr3, Constructions):
                                for instr4 in instr3.Constr.instructions:
                                    if isinstance(instr4, Constructions):
                                        pass
                                    else:
                                        self.file.writelines(
                                            self.building_for(
                                                instr.Constr.init['name'],
                                                self.lt_or_gt(
                                                    instr.Constr.init['value'],
                                                    eval(instr.Constr.end_condition['value'])
                                                ),
                                                instr.Constr.init['value'],
                                                instr.Constr.increment['inc'],
                                                instr.Constr.end_condition['value'],
                                                self.building_for(
                                                    instr2.Constr.init['name'],
                                                    self.lt_or_gt(
                                                        instr2.Constr.init['value'],
                                                        eval(instr2.Constr.end_condition['value'])
                                                    ),
                                                    instr2.Constr.init['value'],
                                                    instr2.Constr.increment['inc'],
                                                    instr2.Constr.end_condition['value'],
                                                    self.building_for(
                                                        instr3.Constr.init['name'],
                                                        self.lt_or_gt(
                                                            instr3.Constr.init['value'],
                                                            eval(instr3.Constr.end_condition['value'])
                                                        ),
                                                        instr3.Constr.init['value'],
                                                        instr3.Constr.increment['inc'],
                                                        instr3.Constr.end_condition['value'],
                                                        self.creating_two_dimensional_array(
                                                            '',
                                                            instr4['var'],
                                                            'i',
                                                            'j'
                                                        ) + "=" + instr4['val'] + ";\n\t"
                                                    )
                                                )
                                            )
                                        )
                            else:
                                self.file.writelines(
                                    self.building_for(
                                        instr.Constr.init['name'],
                                        self.lt_or_gt(
                                            instr.Constr.init['value'],
                                            eval(instr.Constr.end_condition['value'])
                                        ),
                                        instr.Constr.init['value'],
                                        instr.Constr.increment['inc'],
                                        instr.Constr.end_condition['value'],
                                        self.building_for(
                                            instr2.Constr.init['name'],
                                            self.lt_or_gt(
                                                instr2.Constr.init['value'],
                                                eval(instr2.Constr.end_condition['value'])
                                            ),
                                            instr2.Constr.init['value'],
                                            instr2.Constr.increment['inc'],
                                            instr2.Constr.end_condition['value'],
                                            self.creating_two_dimensional_array(
                                                '',
                                                instr3['var'],
                                                'i',
                                                'j'
                                            ) + "=" + instr3['val'] + ";\n\t"
                                        )
                                    )
                                )
        self.building_cuda()

    def building_cuda(self):
        mainCudaFunc1 = "\t{0}(({1} **)&{2}, sizeof(int) * {3}* {4});\n".format(
            functions[2], keyWords[4], variables[13], variables[11], variables[12])
        self.file.writelines(mainCudaFunc1)

        mainCudaFunc2 = "\t{0}({1}, {2}[0], {3}({4}) * {5} * {6}, {7});\n\n".format(functions[3], variables[13],
                                                                                   variables[14], keyWords[5],
                                                                                   typesVariables[0], variables[11],
                                                                                   variables[12], functions[4])
        self.file.writelines(mainCudaFunc2)

        mainCudaFunc3 = "\t{0}<<<{1},{1}>>>({2});\n\n".format(
            functions[0], variables[0], variables[13])
        self.file.writelines(mainCudaFunc3)

        mainCudaFunc4 = "\t{0}({2}[0], {1}, {3}({4}) * {5} * {6}, {7});\n".format(functions[3], variables[13],
                                                                                     variables[14], keyWords[5],
                                                                                     typesVariables[0], variables[11],
                                                                                     variables[12], functions[5])
        self.file.writelines(mainCudaFunc4)

        # free memory
        self.file.writelines("\n\tdelete A[0];\n\tdelete A;\n\tcudaFree(dA);\n}")

    def building_headers(self):

        for i, lib in enumerate(libraries):
            if libraries and i != 0:
                self.file.writelines("{0} {1}\n".format(libraries[0], lib))
        self.file.writelines('\n')

        if self.phrase.variables:
            for dist in self.phrase.variables:
                if 'value' in self.phrase.variables[dist]:
                    self.file.writelines("{0} {1} {2}\n".format(
                        keyWords[0], dist, self.phrase.variables[dist]['value']))
                if 'size' in self.phrase.variables[dist]:
                    self.file.write("\n{0} {1}".format(keyWords[0], dist))
                    for elem in range(len(self.phrase.variables[dist]['size'])):
                        self.file.write("[{0}]".format(self.phrase.variables[dist]['size'][elem]))
            self.file.writelines('\n')

        for i, nmsp in enumerate(namespaces):
            if namespaces and i != 0:
                self.file.writelines("{0} {1};\n".format(namespaces[0], nmsp))
        self.file.writelines('\n')

        # typedef int arrtype[N];
        if self.phrase.variables:
            for dist in self.phrase.variables:
                if 'value' in self.phrase.variables[dist]:
                    self.file.writelines('{};\n'.format(
                        self.creating_one_dimensional_array(
                            self.phrase.variables[dist]['dtype'],
                            variables[1],
                            dist,
                            keyWords[1]
                        ),
                    ))
        self.file.writelines('\n')

    def building_kernel(self):
        # MyKernel function is only one and have 0 index in libs
        # main function have 1 index in libs
        # mykernel other functions have indexes 1<10
        # other functions have indexes 10<
        # TODO: is Kernel func always global?

        absolute_json_file_path = 'libs/kernel.json'
        with open(absolute_json_file_path, 'r') as f:
            variables_kernel = json.load(f)

        self.file.writelines(
            "\n\n" + self.creating_function("__global__ " + keyWords[4], functions[0], '', 'int d_a[r1][c1],int d_b[r2][c2],int d_mult[r1][c2]') + "\n")


        # myKernelFunc = "\n{0} {1} {2}({3} {4}[{5}][{6}]){{\n\n".format(
        #     keyWords[3], keyWords[4], functions[0], typesVariables[0], variables[7], variables[0], variables[0])
        # self.file.writelines(myKernelFunc)

        myKernelBody1 = "\t{0} {1} = {2}.y * {3}.y + {4}.y; \n\t{5} {6} = {7}.x * {8}.x + {9}.x; \n\n".format(
            typesVariables[0], variables[2], variables[8], variables[9], variables[10],
            typesVariables[0], variables[3], variables[8], variables[9], variables[10])
        self.file.writelines(myKernelBody1)

        if variables_kernel:
            for variable in variables_kernel['kernel']:
                if variable['value']:
                    self.file.writelines("\t" + self.declaration_variable_with_value(
                        variable['type'], variable['name'], variable['value']) + ";")
                else:
                    self.file.writelines("\t" + self.declaration_variable(
                        variable['type'], variable['name']) + ";")
                self.file.writelines('\n')

        myKernelIf = "\tif(row >= h || col >= w)\n\t\t{4};\n\n\t".format(
            variables[4], variables[6], variables[5], variables[7], keyWords[2])
        self.file.writelines(myKernelIf)

        # recznie trzeba usunac najbardziej zewnetrzna petle i zmienic idnex i na threadIdx
        for instr in self.phrase.instructions:
            if isinstance(instr, Constructions):
                for instr2 in instr.Constr.instructions:
                    if isinstance(instr2, Constructions):
                        for instr3 in instr2.Constr.instructions:
                            if isinstance(instr3, Constructions):
                                for instr4 in instr3.Constr.instructions:
                                    if isinstance(instr4, Constructions):
                                        pass
                                    else:
                                        self.file.writelines(
                                            self.building_for(
                                                instr.Constr.init['name'],
                                                self.lt_or_gt(
                                                    instr.Constr.init['value'],
                                                    eval(instr.Constr.end_condition['value'])
                                                ),
                                                instr.Constr.init['value'],
                                                instr.Constr.increment['inc'],
                                                instr.Constr.end_condition['value'],
                                                self.building_for(
                                                    instr2.Constr.init['name'],
                                                    self.lt_or_gt(
                                                        instr2.Constr.init['value'],
                                                        eval(instr2.Constr.end_condition['value'])
                                                    ),
                                                    instr2.Constr.init['value'],
                                                    instr2.Constr.increment['inc'],
                                                    instr2.Constr.end_condition['value'],
                                                    self.building_for(
                                                        instr3.Constr.init['name'],
                                                        self.lt_or_gt(
                                                            instr3.Constr.init['value'],
                                                            eval(instr3.Constr.end_condition['value'])
                                                        ),
                                                        instr3.Constr.init['value'],
                                                        instr3.Constr.increment['inc'],
                                                        instr3.Constr.end_condition['value'],
                                                        self.creating_two_dimensional_array(
                                                            '',
                                                            instr4['var'],
                                                            'i',
                                                            'j'
                                                        ) + "=" + instr4['val'] + ";\n\t"
                                                    )
                                                )
                                            )
                                        )
                            else:
                                self.file.writelines(
                                    self.building_for(
                                        instr.Constr.init['name'],
                                        self.lt_or_gt(
                                            instr.Constr.init['value'],
                                            eval(instr.Constr.end_condition['value'])
                                        ),
                                        instr.Constr.init['value'],
                                        instr.Constr.increment['inc'],
                                        instr.Constr.end_condition['value'],
                                        self.building_for(
                                            instr2.Constr.init['name'],
                                            self.lt_or_gt(
                                                instr2.Constr.init['value'],
                                                eval(instr2.Constr.end_condition['value'])
                                            ),
                                            instr2.Constr.init['value'],
                                            instr2.Constr.increment['inc'],
                                            instr2.Constr.end_condition['value'],
                                            self.creating_two_dimensional_array(
                                                '',
                                                instr3['var'],
                                                'i',
                                                'j'
                                            ) + "=" + instr3['val'] + ";\n\t"
                                        )
                                    )
                                )

        self.file.writelines('\n}')

    def building_file(self):
        logger.info('Started file building')
        self.check_variables_type2(self.phrase.variables)

        self.building_headers()
        self.building_kernel()
        self.building_main()
