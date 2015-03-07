import Parser

parser = Parser.Parser()

parser.start('./Test.org')
parser.write('./output.org')
