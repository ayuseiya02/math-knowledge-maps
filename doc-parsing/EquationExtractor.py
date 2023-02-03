def extractEquation(xml_filename, eqn_filename):
    xml_file = open(xml_filename, "r").read()
    eqn_file = open(eqn_filename, "w")

    eqn_file.write("<root>\n\n")
    
    math_tag_start = xml_file.find("<math")
    math_tag_end = xml_file.find("</math>") + len("</math>")

    while math_tag_start != -1:
        eqn = xml_file[math_tag_start:math_tag_end]
        if (eqn.find("display=\"block\"") != -1):
            eqn_file.write(eqn)
            eqn_file.write("\n\n")
        
        math_tag_start = xml_file.find("<math", math_tag_end)
        math_tag_end = xml_file.find("</math>", math_tag_end) + len("</math>")

    eqn_file.write("</root>")
