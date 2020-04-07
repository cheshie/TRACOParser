from src import FileBuilder
from src import logger
from Parser.Parser import Parser

if __name__ == "__main__":
    file_name = "Examples/example1.c"
    parsing_phrases = Parser(file_name).readfile()
    filename = 'main'
    FileBuilder(parsing_phrases, filename)
