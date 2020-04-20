import os
import logging

logger = logging.getLogger(__name__)

_ext = '.cu'

lib_folder = os.getcwd()+'/libs'
if not os.path.exists(lib_folder):
    os.makedirs(lib_folder)
prod_folder = os.getcwd()+'/Products'
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
    def __init__(self, phrase, filename):
        logger.info('Initialized FileBuilder')
        self.phrase = phrase
        self.make_file(filename)

    def make_file(self, filename):
        f = open('{0}/{1}{2}'.format(prod_folder, filename, _ext), 'w+')
        self.building_file(f)
        f.close()
        logger.info('Created file')

    def check_variables_type(self):
        logger.info("Checking the type of variables")
        if self.phrase.variables:
            for var in self.phrase.variables:
                if type(self.phrase.variables[var]) is not dict:
                    logger.warn('var: {} is {} type'.format(
                        var, type(self.phrase.variables[var])))
                if type(self.phrase.variables[var]) is dict:
                    logger.warn('{} is matrix'.format(var))
        else:
            logger.warn('no variables')

    # building_for - function to create loop for
    # variable - loop's variable
    # condition - condition's variable
    # start - init value
    # step - step in loop
    # stop - end value
    # inside - loop body
    def building_for(self, variable, condition, start, step, stop, inside=''):
        return f"for({variable} = {start}; {variable} {condition} {stop}; {variable} += {variable} + {step}) {{ \n\t{inside} }}"

    # declaration_variable_with_value - function to create variable with value
    # type - variable type
    # name - variable name
    # value - init value
    def declaration_variable_with_value(self, type, name, value):
        return f"{type} {name} = {value}"

    # declaration_variable - function to create variable
    # type - variable type
    # name - variable name
    def declaration_variable(self, type, name):
        return f"{type} {name}"

    # creating_function - function to create function
    # returnType - return variable type
    # name - function name
    # typedef - definition typedef
    # param - parameters taken by the function
    def creating_function(self, returnType, name, typedef='', param=''):
        return f"{typedef} {returnType} {name}({param}) {{ "

    # creating_two_dimensional_array - function to create two dimensional array
    # type - array type
    # name - array name
    # first_dim - first dimension of the array
    # second_dim - second dimension of the array
    def creating_two_dimensional_array(self, type, name, first_dim, second_dim):
        return f"{type} {name}[{first_dim}][{second_dim}]"

    # creating_one_dimensional_array - function to create array
    # type - array type
    # name - array name
    # first_dim - first dimension of the array
    # typedef - definition typedef
    def creating_one_dimensional_array(self, type, name, first_dim, typedef=''):
        return f"{typedef} {type} {name}[{first_dim}]"

    # lt_or_gt - function for determining the sign "less than" or "greater than"
    # type - variable type
    # name - variable name
    def lt_or_gt(self, startValue, endValue):
        if startValue < endValue:
            return '<'
        else:
            return '>'

    def building_file(self, file):
        logger.info('Started file building')
        self.check_variables_type()
        definitionLib = "\n{0} {1}\n".format(libraries[0], libraries[1])
        file.writelines(definitionLib)

        #
        # file.writelines(self.building_for('x', '<=', 1, 2, 10, self.building_for('y', '<', 1, 2, 10)))
        # file.writelines(self.declaration_variable_with_value('int', 'N', 8) + ";\n")
        # file.writelines(self.declaration_variable('int', 'N') + ";\n")
        # file.writelines(self.creating_function('void', 'main', '__global__', self.declaration_variable('arrtype', '*dA')) + ";\n")
        # file.writelines(self.creating_two_dimensional_array('int', 'd_A','N', 'N') + ";\n")

        definitionConst = "\n{0} {1} {2} \n\n".format(
            keyWords[0], variables[0], values[0])
        file.writelines(definitionConst)

        file.writelines(namespaces)

        # typedef int arrtype[N];
        file.writelines("\n" + self.creating_one_dimensional_array(typesVariables[0], variables[1], variables[0], keyWords[1]) + ";\n")

        myKernelFunc = "\n{0} {1} {2}({3} {4}[{5}][{6}]){{\n\n".format(
            keyWords[3], keyWords[4], functions[0], typesVariables[0], variables[7], variables[0], variables[0])
        file.writelines(myKernelFunc)
        myKernelBody1 = "\t{0} {1} = {2}.y * {3}.y + {4}.y; \n\t{5} {6} = {7}.x * {8}.x + {9}.x; \n\n".format(
            typesVariables[0], variables[2], variables[8], variables[9], variables[10], typesVariables[0], variables[3], variables[8], variables[9], variables[10])
        file.writelines(myKernelBody1)

        definitionVariable2 = "\t{0} {1} = {2};\n\t{3} {4} = {5};\n\t{6} {7};\n\t".format(
            typesVariables[0], variables[4], variables[0], typesVariables[0], variables[5], variables[0], typesVariables[0], variables[6])
        file.writelines(definitionVariable2)

        myKernelIf = "if({0} >= {1} || {2} >= {3})\n\t\t{4};\n\n\t".format(
            variables[4], variables[6], variables[5], variables[7], keyWords[2])
        file.writelines(myKernelIf)

        myKernelFor = "for({0}={1};{0}<{2};{0}++)\n\t\t{3}[{4}][{0}] = {5}\n\n}}".format(
            variables[6], values[2], variables[0], variables[0], variables[10], values[1])
        file.writelines(myKernelFor)

        # int main() {
        file.writelines("\n\n" + self.creating_function(typesVariables[0], functions[1], '', '') + "\n")

        # int rows = N;
        # int cols = N;
        # arrtype *dA;
        file.writelines("\t" + self.declaration_variable_with_value(typesVariables[0], variables[11], variables[0]) + ";\n")
        file.writelines("\t" + self.declaration_variable_with_value(typesVariables[0], variables[12], variables[0]) + ";\n")
        file.writelines("\t" + self.declaration_variable(variables[1], '*d') + ";\n")

        # int** A = new int*[rows];
        file.writelines("\t" + self.declaration_variable_with_value(typesVariables[2], variables[14], self.creating_one_dimensional_array('new', typesVariables[2], variables[11])) + ";\n")

        # A[0] = new int[rows * cols];
        file.writelines("  " + self.creating_one_dimensional_array('', variables[14], 0) + "=" + self.creating_one_dimensional_array('new', typesVariables[0], 'rows*cols') + ";\n")

        # for (int i = 1; i < rows; ++i) { A[i] = A[i-1] + cols; };
        file.writelines("\n\t" + self.building_for('i', self.lt_or_gt(1, 10), 1, 1, variables[11], self.creating_one_dimensional_array('', variables[14], 0) + "=" + self.creating_one_dimensional_array('', variables[14],'i-1') + " + cols;\n\t") + ";\n")

        # for (int i = 0; i < rows; ++i) { for (int j = 0; j < cols; ++j) { A[i][j] = i*cols+j; }; };
        file.writelines("\n\t" + self.building_for('x', self.lt_or_gt(1, 10), 1, 2, 10, self.building_for('y', '<', 1, 2, 10, self.creating_two_dimensional_array('', 'A','N', 'N') + "= i*cols+j;\n\t") + ";\n\t") + ";\n")

        mainCudaFunc1 = "\t{0}(({1}**)&{2}, sizint) * {3}* {4});\n".format(
            functions[2], keyWords[4], variables[13], variables[11], variables[12])
        file.writelines(mainCudaFunc1)

        mainCudaFunc2 = "\t{0}({1}, {2}[0], {3}({4}) * {5}* {6}, {7});\n\n".format(functions[3], variables[13],
                                                                                   variables[14], keyWords[5], typesVariables[0], variables[11], variables[12], functions[4])
        file.writelines(mainCudaFunc2)

        mainCudaFunc3 = "\t{0} <<{1},{1}>>({2});\n\n".format(
            functions[0], variables[0], variables[13])
        file.writelines(mainCudaFunc3)

        mainCudaFunc4 = "\t{0}({2}[0], {1}, {3}({4}) * {5}* {6}, {7});\n\n}}".format(functions[4], variables[13],
                                                                                     variables[14], keyWords[5], typesVariables[0], variables[11], variables[12], functions[5])
        file.writelines(mainCudaFunc4)
