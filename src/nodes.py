#!/usr/bin/env python
# NODES


class CallNode():
    """docstring for CallNode"""

    def __init__(self, name, arg_exprs):
        self.name = name
        self.arg_exprs = arg_exprs

    def __str__(self):
        return '<class CallNode name=%s, arg_exprs=\"%s\" \n' % (self.name, 
                                                                 self.arg_exprs)

class IntegerNode():
    """docstring for IntegerNode"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '<class IntegerNode value=\"%s\" \n' % (self.value)
    
    def __repr__(self):
        return self.value

class FloatNode():
    """docstring for FloatNode"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '<class FloatNode value=\"%s\" \n' % (self.value)

class StringNode():
    """docstring for StringNode"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '<class StringNode value=\"%s\" \n' % (self.value)

class SymbolNode():
    """docstring for SymbolNode"""

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return '<class SymbolNode symbol=\"%s\" \n' % (self.symbol)            

class VarNode():
    """docstring for VarNode"""

    def __init__(self, value):
        self.value = value

    # def __str__(self):
    #     return '<class VarNode value=\"%s\" \n' % (self.value) 
    
    def __repr__(self):
        return self.value

class AssignmentNode():
    """docstring for AssignmentNode"""

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return '<class AssignmentNode lhs=%s, rhs=\"%s\" \n' % (self.lhs, 
                                                                self.rhs)

class ConditionalNode():
    """docstring for ConditionalNode"""

    def __init__(self, type, cond):
        self.type = type
        self.condition = cond

    def __str__(self):
        return '<class ConditionalNode type=%s, condition=\"%s\" \n' % (self.type, 
                                                                        self.condition)


class ConditionNode():
    """docstring for ConditionNode"""

    def __init__(self, comparation_nodes, logical_nodes):
        self.comparation_nodes = comparation_nodes
        self.logical_nodes = logical_nodes

    def __str__(self):
        return '<class ConditionNode comparation_nodes=%s, logical_conds=\"%s\" \n' % (self.comparation_nodes, 
                                                                                       self.logical_nodes)

class ComparationNode():
    """docstring for ComparationNode"""

    def __init__(self, lhs, comp, rhs):
        self.lhs = lhs
        self.comp = comp
        self.rhs = rhs

    def __str__(self):
        return '<class ComparationNode lhs=%s, comp=%s, rhs=\"%s\" \n' % (self.lhs, 
                                                                          self.comp, 
                                                                          self.rhs)

class LogicalConditionNode():
    """docstring for LogicalConditionNode"""

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return '<class LogicalConditionNode type=\"%s\" \n' % (self.type)


class Body():
    """docstring for Body"""

    def __init__(self, assignments, condition_statements, ordenation):
        self.assignments = assignments
        self.condition_statements = condition_statements
        self.ordenation = ordenation

    def __str__(self):
        return '<class Body assignments=%s, condition_statements=%s, ordenation=\"%s\" \n' % (self.assignments, 
                                                                                              self.condition_statements, 
                                                                                              self.ordenation)

class DatasetNode():
    """docstring for DatasetNode"""

    def __init__(self, itable_name, otable_name, body):
        self.input = itable_name
        self.output = otable_name
        self.body = body

    def __str__(self):
        return '<class DatasetNode input=%s, output=%s, body=\"%s\" \n' % (self.input, 
                                                                           self.output, 
                                                                           self.body)