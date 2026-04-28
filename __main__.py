from parser.parser import parser
from lexer.lexer import lexer
import pprint
import sys
from executor.engine import CSVEngine



if __name__ == "__main__":
    engine = CSVEngine("queries.sql")
    engine.parse()
    engine.print_queries()