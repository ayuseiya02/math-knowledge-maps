def matchTags(html_filename, xml_filename):
    html_file = open(html_filename, "r")
    xml_file = open(xml_filename, "w")

    tag = ""
    start_tags = []

    in_tag = False
    in_comment = False
    just_started = False
    is_end_tag = False

    while True:
        c = html_file.read(1)

        if not c:
            break

        if in_tag and is_end_tag:
            if c == ">":
                mismatch = False
                while start_tags[-1] != tag:
                    mismatch = True
                    xml_file.write(start_tags[-1] + ">\n</")
                    start_tags.pop(-1)
                #if mismatch:
                    #xml_file.write("</")
                xml_file.write(start_tags[-1] + ">")
                start_tags.pop(-1)
                is_end_tag = False
                in_tag = False
                tag = ""
            else:
                tag += c
        else:
            if in_comment:
                if c == ">":
                    in_comment = False
                    in_tag = False
            elif in_tag:
                if just_started:
                    if c == "!":
                        in_comment = True
                    elif c == "/":
                        is_end_tag = True
                    else:
                        tag += c
                    just_started = False
                else:
                    if c == " " or c == ">":
                        start_tags.append(tag)
                        #print("tag: " + tag)
                        in_tag = False
                        tag = ""
                    else:
                        tag += c
            elif c == "<":
                in_tag = True
                just_started = True
            xml_file.write(c)

    xml_file.close()
    html_file.close()

HTML_AMP_CHARS = {
    "&quot;", "&amp;", "&lt;", "&gt;", "&nbsp;", "&iexcl;", "&cent;", "&pound;",
    "&curren;", "&yen;", "&brvbar;", "&sect;", "&uml;", "&copy;", "&ordf;",
    "&laquo;", "&not;", "&shy;", "&reg;", "&macr;", "&deg;", "&plusmn;", "&sup2;",
    "&sup3;", "&acute;", "&micro;", "&para;", "&middot;", "&cedil;", "&sup1;",
    "&ordm;", "&raquo;", "&frac14;", "&frac12;", "&frac34;", "&iquest;", "&times;",
    "&divide;", "&ETH;", "&eth;", "&THORN;", "&thorn;", "&AElig;", "&aelig;",
    "&OElig;", "&oelig;", "&Aring;", "&Oslash;", "&Ccedil;", "&ccedil;", "&szlig;",
    "&Ntilde;", "&ntilde;"
}
def findOccurrences(s, c):
    return [i for i, lett in enumerate(s) if lett == c]

def fixAmpersands(xml_filename):
    xml_file = open(xml_filename, "r")

    replaced_content = ""
    lines = xml_file.readlines()
    for line in lines:
        occurrences = findOccurrences(line, "&")
        invalid_amps = []
        for occur in occurrences:
            idx = occur
            amp_string = ""
            add_semi = True
            while line[idx] != ";" and idx - occur < len(max(HTML_AMP_CHARS)):
                amp_string += line[idx]
                idx += 1

                if idx >= len(line):
                    add_semi = False
                    break
            if add_semi:
                amp_string += ";"

            if amp_string not in HTML_AMP_CHARS:
                invalid_amps.append(occur)
        
        new_line = line
        for i in range(len(invalid_amps)):
            idx = invalid_amps[len(invalid_amps) - i - 1]
            new_line = new_line[:idx + 1] + "amp;" + new_line[idx + 1:]
        replaced_content += new_line

    xml_file.close()

    xml_file = open(xml_filename, "w")
    xml_file.write(replaced_content)
    xml_file.close()

def convertHtmlToXml(html_filename, xml_filename):
    matchTags(html_filename, xml_filename)
    fixAmpersands(xml_filename)    
