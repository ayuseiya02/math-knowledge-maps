import os
from EquationExtractor import *

for filename in os.listdir("../articles/xml"):
    extractEquation("../articles/xml/" + filename, "equations/" + filename[:-4] + "-eqns.xml")