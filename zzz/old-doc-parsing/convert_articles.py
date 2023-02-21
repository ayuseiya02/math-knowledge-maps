import os
from HtmlToXmlConverter import *

for filename in os.listdir("../data/html"):
    convertHtmlToXml("../data/html/" + filename, "../data/xml/" + filename[:-5] + ".xml")