import sys

from MathMLToOpTree import *   
from StandardizeOpTree import *

test_filename = "tests/custom/basic1.xml" # default test file
if len(sys.argv) > 1: # but will run diff test file if one is passed as argument
    test_filename = sys.argv[1]
plotTreesFromFile(test_filename)

