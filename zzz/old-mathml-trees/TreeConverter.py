import xml.sax
import networkx as nx

def convertToTrees(file):
    class ArxivHandler( xml.sax.ContentHandler ):
        def __init__(self):
            self.in_eqn = False
            self.in_ident = False
            self.in_num = False
            self.in_op = False

            self.in_cn = False
            self.in_ci = False
            self.in_csymbol = False

            self.curr_tree = None
            self.curr_parent = None
            self.curr_node = None

            self.trees = []

        def startElement(self, name, attrs):
            if name == "root":
                return

            if name == "math":
                self.in_eqn = True

                self.curr_tree = nx.DiGraph()

                new_node = len(self.curr_tree.nodes)
                self.curr_tree.add_node(new_node, data = name)

                self.curr_node = new_node

            else:
                if name == "mi":
                    self.in_ident = True
                if name == "mn":
                    self.in_num = True
                if name == "mo":
                    self.in_op = True
                
                if name == "cn":
                    self.in_cn = True
                if name == "ci":
                    self.in_ci = True
                if name == "csymbol":
                    self.in_csymbol = True

                new_node = len(self.curr_tree.nodes)
                self.curr_tree.add_node(new_node, data = name)
                
                self.curr_parent = self.curr_node
                self.curr_node = new_node

                self.curr_tree.add_edge(self.curr_parent, self.curr_node)
        
        def endElement(self, name):
            if name == "root":
                return 

            if name == "math":
                self.in_eqn = False
                self.in_ident = False
                self.in_num = False
                self.in_op = False

                self.trees.append(self.curr_tree)

                self.curr_tree = None
                self.curr_parent = None
                self.curr_node = None

            else:
                if name == "mi":
                    self.in_ident = False
                if name == "mn":
                    self.in_num = False
                if name == "mo":
                    self.in_op = False

                if name == "cn":
                    self.in_cn = False
                if name == "ci":
                    self.in_ci = False
                if name == "csymbol":
                    self.in_csymbol = False

                self.curr_node = self.curr_parent
                for pred in self.curr_tree.predecessors(self.curr_node):
                    self.curr_parent = pred

        def characters(self, chars):
            if self.in_eqn and (self.in_ident or self.in_num or self.in_op
                                or self.in_cn or self.in_ci or self.in_csymbol):
                new_node = len(self.curr_tree.nodes)

                self.curr_tree.add_node(new_node, data = chars)
                self.curr_tree.add_edge(self.curr_node, new_node)

    parser = xml.sax.make_parser()
    Handler = ArxivHandler()
    parser.setContentHandler(Handler)
    parser.parse(file)

    return Handler.trees
            
