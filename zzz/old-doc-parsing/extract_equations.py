import os
from EquationExtractor import *

for filename in os.listdir("../data/xml"):
    extractEquation("../data/xml/" + filename, "../data/xml-eqns/" + filename[:-4] + "-eqns.xml")