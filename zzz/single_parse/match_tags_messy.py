html_file = open("test.html", "r")
xml_file = open("test.xml", "w")

tag = ""
start_tags = []

in_tag = False
just_started = False
is_start_tag = False
in_comment = False

while 1:
    c = html_file.read(1)

    if not c:
        break
    
    if c == "<":
        in_tag = True
        just_started = True
        xml_file.write(c)
    elif in_comment:
        if c == ">":
            in_comment = False
            in_tag = False
        xml_file.write(c)
    elif in_tag:
        if just_started:
            if c == "!":
                in_comment = True
                xml_file.write(c)
            elif c != "/":
                is_start_tag = True
                tag += c
            else:
                xml_file.write(c)
            just_started = False
        else:
            if c == " " or c == ">":
                if is_start_tag:
                    start_tags.append(tag)
                    print("tag: " + tag)
                    xml_file.write(tag + c)
                else:
                    mismatch = False
                    while len(start_tags) > 0 and start_tags[-1] != tag:
                        mismatch = True
                        xml_file.write(start_tags[-1] + ">")
                        start_tags.pop(-1)
                    if mismatch:
                        xml_file.write("</")
                        mismatch = False
                    xml_file.write(tag + ">")
                    start_tags.pop(-1)
                is_start_tag = False
                in_tag = False
                tag = ""
            else: 
                tag += c
    else:
        xml_file.write(c)
        
        