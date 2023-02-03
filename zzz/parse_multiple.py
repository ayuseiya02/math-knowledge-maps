import os
import XMLConverter
import parse

def output_to_tex(tex_filename, all_eqns, threshold):
    eqn_file = open(tex_filename, "w")

    eqn_file.write("\\documentclass{article}\n")
    eqn_file.write("\\usepackage{lmodern}\n")
    eqn_file.write("\\usepackage{newtxmath}\n")
    eqn_file.write("\\begin{document}\n")
    eqn_file.write("Equations that appear in at least " + str(threshold) + " articles:\n")
    
    for eqn in all_eqns:
        if len(all_eqns[eqn][0]) >= threshold:
            eqn_file.write("\\begin{equation}\n")

            if len(eqn) > len("\\matrix") and eqn[:len("\\matrix")] == "\\matrix":
                eqn_file.write("\\begin{matrix}\n")
                eqn_file.write(eqn[len("\\matrix") + 1:-1] + "\n")
                eqn_file.write("\\end{matrix}\n")
                eqn_file.write("\\end{equation}\n")
            else:
                eqn_file.write(eqn + "\n")
                eqn_file.write("\\end{equation}\n")

            eqn_file.write("ops found: ")
            eqn_file.write("\\begin{math}")
            for op in all_eqns[eqn][1]:
                eqn_file.write(op + ", ")
            eqn_file.write("\\end{math}\\\\\n")

            eqn_file.write("appears in: ")
            for file in all_eqns[eqn][0]:
                eqn_file.write(file[:-4] + ", ")
            eqn_file.write("\n")

    eqn_file.write("\\end{document}")

    eqn_file.close()

def parse_multiple(directory, tex_filename, threshold, 
                    skip_html_to_xml_conversion = False):

    if not skip_html_to_xml_conversion:
        article_ct = len(os.listdir(directory + "articles_html/"))
        for filename in os.listdir(directory + "articles_html/"):
            print(str(article_ct) + " articles left to convert")
            article_ct -= 1
            
            XMLConverter.html_to_xml(directory + "articles_html/" + filename, 
                                    directory + "articles_xml/" + filename[:-5] + ".xml")

    all_eqns = {}
    article_ct = len(os.listdir(directory + "articles_xml/"))
    for filename in os.listdir(directory + "articles_xml/"):
        print(str(article_ct) + " articles left to parse")
        article_ct -= 1

        parsed_file = parse.parse_xml(directory + "articles_xml/" + filename)
        for eqn in parsed_file.eqns:
            if eqn in all_eqns:
                all_eqns[eqn][0].append(filename)
            else:
                all_eqns[eqn] = [[filename], parsed_file.ops_in_eqns[eqn]]

    output_to_tex(tex_filename, all_eqns, threshold)

parse_multiple("/Users/ayuseiya/projects/official/knowledge-maps/",
                "/Users/ayuseiya/projects/official/knowledge-maps/multiple_eqns.tex",
                2,
                True)
