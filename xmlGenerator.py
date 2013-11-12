import ast

# Maybe use ET?
import xml.etree.ElementTree as ET

class indexVisitor(ast.NodeVisitor):
    def __init__(self):
        self.coeff = 1
        self.offset = 0
        self.var = ''

    def visit_Name(self, node):
        self.var = node.id

    def visit_Num(self,node):
        return node.n

    def visit_BinOp(self, node):
        if type(node.op) == ast.Mult:
            if type(node.left) == ast.Num:
                self.coeff = self.visit(node.left)
            else:
                self.coeff = self.visit(node.right)
        elif type(node.op) == ast.Div:
            if type(node.left) == ast.Num:
                self.coeff = 1 / self.visit(node.left)
            else:
                self.coeff = 1 / self.visit(node.right)
        elif type(node.op) == ast.Add:
            if type(node.left) == ast.Num:
                self.offset = self.visit(node.left)
            else:
                self.offset = self.visit(node.right)
        elif type(node.op) == ast.Sub:
            if type(node.left) == ast.Num:
                self.coeff = -self.visit(node.left)
            else:
                self.coeff = -self.visit(node.right)

        self.generic_visit(node)

class xmlGenerator(ast.NodeVisitor):

    def __init__(self, args_info):
        """
        args_info = {args_name : (args_type, [args_dim])}
        """
        self.args_info = args_info;
        self.xmlstr = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        self.binaryOp = { ast.Add : 'ADD', ast.Mult : 'MUL' }
        self.in_subscript = False

    def write(self, name):
        f = open(name, 'w')
        f.write(self.xmlstr)
        f.close()

    def visit_FunctionDef(self, node):
        self.xmlstr += '<program>\n'
        self.xmlstr += '<Name>' + node.name + '</Name>\n'
        self.generic_visit(node);
        self.xmlstr += '</program>\n'

    def visit_arguments(self, node):
        for args in node.args:
            self.xmlstr += '<Var>\n'
            self.xmlstr += '<Name>' + str(args.id) + '</Name>\n'
            self.xmlstr += '<Type>' + str(self.args_info[args.id][0]) + '</Type>'
            for dim in self.args_info[args.id][1]:
                self.xmlstr += '<Dim>' + str(dim) + '</Dim>'
            self.xmlstr += '</Var>\n'

    def visit_Name(self, node):
        self.xmlstr += str(node.id)

    def visit_Num(self, node):
        self.xmlstr += '<Constant>\n'
        self.xmlstr += '<Name>' + str(id(node)) + '</Name>\n'
        self.xmlstr += '<Value>' + str(node.n) + '</Value>\n'
        self.xmlstr += '</Constant>\n'

    def visit_For(self, node):
        self.xmlstr += '<ForStmt>\n'
        self.xmlstr += '<LoopHeader>\n'
        
        self.xmlstr += '<Name>' + str(id(node)) + '</Name>\n'

        self.xmlstr += '<Induction>'
        self.visit(node.target)
        self.xmlstr += '</Induction>\n'

        self.xmlstr += '<Start>'
        start = node.iter.args[0];
        if type(start) == ast.Num:
            self.xmlstr += str(start.n)
        elif type(start) == ast.Name:
            self.xmlstr += str(start.id)
        self.xmlstr += '</Start>\n'
        
        self.xmlstr += '<Stop>'
        stop = node.iter.args[1];
        if type(stop) == ast.Num:
            self.xmlstr += str(stop.n)
        elif type(stop) == ast.Name:
            self.xmlstr += str(stop.id)
        self.xmlstr += '</Stop>\n'
        
        self.xmlstr += '</LoopHeader>\n'

        self.xmlstr += '<LoopBody>\n'
        for b in node.body:
            self.visit(b)
        self.xmlstr += '</LoopBody>\n'

        self.xmlstr += '</ForStmt>\n'

    def visit_Subscript(self, node):
        if not self.in_subscript:
            self.in_subscript = True
            self.xmlstr += '<MemRef>\n'
            self.xmlstr += '<Name>' + str(id(node)) + '</Name>\n'

            if type(node.value) == ast.Name:
                self.xmlstr += '<Var>'
                self.xmlstr += str(node.value.id)
                self.xmlstr += '</Var>\n'
                self.visit(node.slice)
            else:
                self.generic_visit(node)

            self.xmlstr += '</MemRef>\n'
            self.in_subscript = False
        else:
            if type(node.value) == ast.Name:
                self.xmlstr += '<Var>'
                self.xmlstr += str(node.value.id)
                self.xmlstr += '</Var>\n'
                self.visit(node.slice)
            else:
                self.generic_visit(node)

    def visit_Index(self, node):
        self.xmlstr += '<Subscript>\n'

        iVisitor = indexVisitor()
        iVisitor.visit(node)

        self.xmlstr += '<IndVar>'
        self.xmlstr += iVisitor.var
        self.xmlstr += '</IndVar>\n'

        self.xmlstr += '<IndCoeff>'
        self.xmlstr += str(iVisitor.coeff)
        self.xmlstr += '</IndCoeff>\n'

        self.xmlstr += '<Offset>'
        self.xmlstr += str(iVisitor.offset)
        self.xmlstr += '</Offset>\n'

        self.xmlstr += '</Subscript>\n'

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        
        self.xmlstr += '<CompoundExpr>'
        self.xmlstr += '<Name>' + str(id(node)) + '</Name>\n'
        self.xmlstr += '<Op>' + self.binaryOp[type(node.op)] + '</Op>\n'
        self.xmlstr += '<Left>' + str(id(node.left)) + '</Left>\n'
        self.xmlstr += '<Right>' + str(id(node.right)) + '</Right>\n'
        self.xmlstr += '</CompoundExpr>\n'

    def visit_Assign(self, node):
        self.visit(node.value)
        self.visit(node.targets[0])
        self.xmlstr += '<AssignExpr>'
        self.xmlstr += '<Name>' + str(id(node)) + '</Name>\n'
        self.xmlstr += '<Left>' + str(id(node.targets[0])) + '</Left>\n'
        self.xmlstr += '<Right>' + str(id(node.value)) + '</Right>\n'
        self.xmlstr += '</AssignExpr>\n'
