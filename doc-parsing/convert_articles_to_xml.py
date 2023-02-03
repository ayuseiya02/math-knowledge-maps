import os
from XMLConverter import *

for filename in os.listdir("../articles/html"):
    convertHtmlToXml("../articles/html/" + filename, "../articles/xml/" + filename[:-5] + ".xml")