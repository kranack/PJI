import Parser

parser = Parser.Parser('../db/database.db', '../output/Test.org')

parser.parse()
parser.write()
