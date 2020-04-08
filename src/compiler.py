#!/usr/bin/env python
# COMPILER 
import re
from nodes import *
from parser import Parser
from tokenizer import *

class Generator():
    """docstring for Generator"""

    

    def __init__(self):

        self.macrovar_rhs = []
        self.macrovar_lhs = []
        self.set_list = []

    def generate(self, node):
        if isinstance(node, DatasetNode):
            output = self.generate(node.output)
            input = self.generate(node.input)
            body = self.generate(node.body)

            query = ";\n".join(self.set_list)
            query +=  f"\nCREATE TABLE {output} AS\n"
            query += f"SELECT\n"
            query += f"{body}"
            query += f"  FROM {input};"

            return query

        elif isinstance(node, Body):
            subquery = list()
            node.assignments = []
            for type in node.ordenation:
                # type==0 -> Conditional Statement
                # type==1 -> Assignment
                if type == 0:
                    lhs = self.generate(assignment.lhs)
                    rhs = self.generate(assignment.lhs)
                    
                    subquery.append(f"       {rhs} AS {lhs}")
                    idx += 1

        elif isinstance(node, VarNode) or \
             isinstance(node, IntegerNode) or \
             isinstance(node, FloatNode) or \
             isinstance(node, StringNode):
            return f"{node.value}".lower_case()

        elif isinstance(node, SymbolNode):
            return f"{node.symbol}"

        elif isinstance(node, CallNode):
            name = self.generate(node.name)
            arg_exprs = [self.generate(arg) for arg in node.arg_exprs]
            result = f"{name}".upper_case() 
            result += "("
            result += ",".join(arg_exprs)
            result += ")"
            return result

        elif isinstance(node, AssignmentNode):
            if len(node.lhs) == 2: # macrovariable declartion
                if node.lhs[0].lower_case() == "let":
                    self.macrovar_lhs.append(node.lhs[1])
                    self.macrovar_rhs.append([self.generate(arg) for arg in node.rhs])
                    return ""
            else:
                lhs = node.lhs
                rhs = [self.generate(arg) for arg in node.rhs]
                return " ".join(rhs) + f" AS {lhs}"
        
        elif isinstance(node, ConditionalNode):
            type = node.type
            condition = self.generate(node.cond)
            if type.lower_case() in ['if', 'else if']:
                result = f"IF({condition},"
            elif type.lower_case() == 'else':
                condition = self.generate(node.cond)
                result = f""
            return result

        elif isinstance(node, ConditionNode):
            node.comparation_nodes # 
            node.logical_nodes # ['AND','OR']
            return result

        elif isinstance(node, ComparitionNode):
            lhs = self.generate(node.lhs)
            rhs = self.generate(node.rhs)
            result = f"{lhs}"
            return result
        
        else:
            raise RuntimeError(
                    "Unexpected node type: {}\n".format(type(node)))

    def __str__(self):
        return '<class Generator type=\"%s\" \n' % (self.type)

if __name__ == '__main__':
    tokens = Tokenizer(open('./test/test1.src', 'r').read()).tokenize()
    for token in tokens:
        print(token)

    tree = Parser(tokens).parse()
    print(tree)

    #generated = Generator.generate(tree)
    #print(generated)




