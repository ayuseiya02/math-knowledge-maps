import xml.sax

SOLO_OPERATORS = {
    "+", "-", "!", "<", ">", "="
}

SLASH_OPERATORS = {
    "\\neg", "\\#", # unary

   "\\nless", "\\ngtr", "\\leq", "\\geq", "\\leqslant", "\\geqslant", "\\nleq", "\\ngeq", "\\nleqslant", 
    "\\ngeqslant", "\\prec", "\\succ", "\\nprec", "\\nsucc", "\\preceq", "\\succeq", "\\npreceq", "\\nsucceq", "\\ll", 
    "\\gg", "\\lll", "\\ggg", "\\subset", "\\supset", "\\subseteq", "\\supseteq", 
    "\\nsubseteq", "\\nsupseteq", "\\sqsubset", "\\sqsupset", "\\sqsubseteq", "\\sqsupseteq", # relational 1

    "\\doteq", "\\equiv", "\\approx", "\\cong", "\\simeq", "\\sim", "\\propto", "\\neq", "\\ne", # relational 2

    "\\parallel", "\\nparallel", "\\asymp", "\\bowtie",	"\\vdash", "\\dashv", "\\in", "\\ni", "\\smile", "\\frown",	 
    "\\models", "\\notin", "\\perp", "\\mid", # relational 3

    "\\pm", "\\cap", "\\diamond", "\\oplus", "\\mp", "\\cup", "\\bigtriangleup", "\\ominus", "\\times", "\\uplus", 
    "\\bigtriangledown", "\\otimes", "\\div", "\\sqcap", "\\triangleleft", "\\oslash", "\\ast", "\\sqcup", "\\triangleright", 
    "\\odot", "\\star", "\\vee", "\\bigcirc",	"\\circ", "\\dagger", "\\wedge", "\\bullet", "\\setminus", "\\ddagger", 
    "\\cdot", "\\wr", "\\amalg" # binary

    "\\cos", "\\csc", "\\exp", "\\ker", "\\limsup", "\\min", "\\sinh", "\\arcsin", "\\cosh", "\\deg",
    "\\gcd", "\\lg", "\\ln", "\\Pr", "\\sup", "\\arctan", "\\cot", "\\det", "\\hom", "\\lim", "\\log", "\\sec",
    "\\tan", "\\arg", "\\coth", "\\dim", "\\liminf", "\\max", "\\sin", "\\tanh", "\\int" # math
}

DOUBLE_SLASH_OPERATORS = {
    "\\not\\subset", "\\not\\supset"
}

def parse_eqn(eqn):
    ops_present = set()

    for SOLO_OP in SOLO_OPERATORS:
        if SOLO_OP in eqn:
            ops_present.add(SOLO_OP)

    dbl_slashed_eqn = eqn
    for DBL_SLASH_OP in DOUBLE_SLASH_OPERATORS:
        if DBL_SLASH_OP in eqn:
            ops_present.add(DBL_SLASH_OP)
            dbl_slashed_eqn = eqn.replace(DBL_SLASH_OP, "")
        
    frags = dbl_slashed_eqn.split("\\")
    for frag in frags:
        if len(frag) == 0:
            continue
        idx = 0
        symbol = "\\"
        while frag[idx].isalpha():
            symbol += frag[idx]
            idx += 1
            if idx >= len(frag):
                break
        
        if symbol in SLASH_OPERATORS:
            ops_present.add(symbol) 
    
    return ops_present


def parse_xml(xml_filename): #, tex_filename):
    class ArxivHandler( xml.sax.ContentHandler ):
        def __init__(self):
            self.eqn_ct = 0
            self.eqns = set()
            self.ops_in_eqns = {}
        
        def startElement(self, name, attrs):
            if name == "math" and attrs["display"] != "inline":
                self.eqn_ct += 1

                eqn = attrs["alttext"].replace("% ", "")
                self.eqns.add(eqn)

                ops = parse_eqn(eqn)
                self.ops_in_eqns[eqn] = ops
            
    parser = xml.sax.make_parser()
    Handler = ArxivHandler()
    parser.setContentHandler(Handler)
    parser.parse(xml_filename)

    return Handler

