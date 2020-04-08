#!/usr/bin/env python
# PARSER

from nodes import *

class Parser:
    """docstring for Parser"""

    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        return self.parse_dataset()

    def parse_dataset(self):
        self.consume('data')
        otable_name = self.parse_table_name()
        #oargs = self.parse_data_args()
        self.consume('semicolon')

        self.consume('set')
        itable_name = self.parse_table_name()
        #iargs = self.parse_set_args()
        self.consume('semicolon')

        body = self.parse_body()
        self.consume('run')
        self.consume('semicolon')

        return DatasetNode(itable_name, otable_name, body)


    def parse_table_name(self):
        result = []

        while self.peek('macrovar'):
            result.append(self.consume('macrovar').value)

        while self.peek('identifier'):
            result.append(self.consume('identifier').value)

        return result

    def parse_body(self):
        order_list = []
        condition_statements = []
        assignments = []
        while not self.peek('run'):
            if self.peek('if') or self.peek('elseif') or self.peek('else'):
                order_list.append(0)
                condition_statements.append(self.parse_if_block())
            elif self.peek('end'):
                self.consume('end')
                self.consume('semicolon')
            else:
                order_list.append(1)
                assignments.append(self.parse_assign())

        return Body(assignments, condition_statements, order_list)
        
    def parse_assign(self):
        lhs = []
        rhs = []

        if self.peek('let'):
            lhs.append(self.consume('let'))

        lhs.append(self.consume('identifier').value)
        self.consume('eq')

        while not self.peek('semicolon'):
            rhs.append(self.parse_expr())

        self.consume('semicolon')

        return AssignmentNode(lhs, rhs)

    def parse_values(self):
    
        if self.peek('integer'):
            return IntegerNode(self.consume('integer').value)
        elif self.peek('float'):
            return FloatNode(self.consume('float').value)
        elif self.peek('string'):
            return StringNode(self.consume('string').value)
        return None

    def parse_syms(self):

        if self.peek('multiply'):
            return SymbolNode(self.consume('multiply').value)
        elif self.peek('plus'):
            return SymbolNode(self.consume('plus').value)
        elif self.peek('minus'):
            return SymbolNode(self.consume('minus').value)
        elif self.peek('division'):
            return SymbolNode(self.consume('division').value)
        else:
            return None

    def parse_macrovar(self):
        if self.peek('macrovar'):
            return MacrovarNode(self.consume('macrovar').value)
        return None

    def parse_call(self):
        """" f([x, y, g(z, w), ...])"""

        name = self.consume('identifier').value
        arg_exprs = self.parse_arg_exprs()
        return CallNode(name, arg_exprs)

    def parse_arg_exprs(self):
        arg_exprs = []

        self.consume('oparen')
        if not self.peek('cparen'):
            arg_exprs.append(self.parse_expr())
            while self.peek('comma'):
                self.consume('comma')
                arg_exprs.append(self.parse_expr())
        self.consume('cparen')
        return arg_exprs
  
    def parse_expr(self):
        syms = self.parse_syms()
        values = self.parse_values()
        macrovar = self.parse_macrovar()
        if values is not None:
            return values
        elif syms is not None:
            return syms
        elif macrovar is not None:
            return macrovar
        elif self.peek('identifier') and self.peek('oparen', 1):
            return self.parse_call()
        elif self.peek('identifier'):
            return self.parse_var_ref()
        else:
            return None

    def parse_var_ref(self):
        value = self.consume('identifier').value
        return VarNode(value)

    def parse_if(self):
        type = self.consume('if').value
        conds = self.parse_conditions()
        self.consume('then')
        if self.peek('do'):
            self.consume('do')
            self.consume('semicolon')
            #body = self.parse_body('end');
        #else:
        #    body = self.parse_body('semicolon');
        return ConditionalNode(type, conds)
    
    def parse_elseif(self):
        type = self.consume('elseif').value
        conds = self.parse_conditions()
        self.consume('then')
        if self.peek('do'):
            self.consume('do')
            self.consume('semicolon')
        return ConditionalNode(type, conds)

    def parse_else(self):
        type = self.consume('else').value
        conds = None
        if self.peek('do'):
            self.consume('do')
            self.consume('semicolon')

        return ConditionalNode(type, conds)

    def parse_if_block(self):
        """ 
        Type 1):
            IF COND THEN DO;
                BODY;
            END;
            ELSE IF COND THEN DO;
                BODY;
            END;
            ELSE DO;
                BODY;
            END;

        Type 2):
            IF COND THEN ASSIGNMENT;
            ELSE IF COND THEN ASSIGNMENT;
            ELSE ASSIGNMENT;
        """
        
        if self.peek('if'):
            return self.parse_if()
        elif self.peek('elseif'):
            return self.parse_elseif()
        elif self.peek('else'):
            return self.parse_else()
        else:
            return None

    def parse_one_condition(self):
        lhs = []
        comp = []
        rhs = []

        expr = 1 # only to get inside the while
        while expr is not None:
            expr = self.parse_expr()
            if expr is not None:
                lhs.append(expr)

        comp = self.parse_comparison()

        expr = 1 # only to get inside the while
        while expr is not None:
            expr = self.parse_expr()
            if expr is not None:
                rhs.append(expr)

        return ComparationNode(lhs, comp, rhs)

    def parse_conditions(self):
        comp_list = []
        logical_cond_list = []
        if self.peek('oparen'):
            self.consume('oparen')
            while not self.peek('cparen'):
                if self.peek('oparen'):
                    comp_list.append(self.parse_conditions())
                else:
                    comp_list.append(self.parse_one_condition())
                    logical_cond_list.append(self.parse_logical_condition())
            self.consume('cparen') 
        else:
            lcond = 1 # only to get inside the while
            while lcond is not None:
                comp_list.append(self.parse_one_condition())
                lcond = self.parse_logical_condition()
                logical_cond_list.append(lcond)

        return ConditionNode(comp_list, logical_cond_list)

    def parse_logical_condition(self):
        type = None
        
        if self.peek('and'):
            type = self.consume('and').value 
        elif self.peek('or'):
            type = self.consume('or').value 
        # elif self.peek('xor'):
        #     type = self.consume('xor').value 

        if type is not None:
            return LogicalConditionNode(type)
        return None

    def parse_comparison(self):

        if self.peek('gt'):
            return self.consume('gt').value
        elif self.peek('lt'):
            return self.consume('lt').value
        elif self.peek('ge'):
            return self.consume('ge').value
        elif self.peek('le'):
            return self.consume('le').value
        elif self.peek('eq'):
            return self.consume('eq').value
        #elif self.peek('ne'):
        #    return self.consume('ne').value
        #elif self.peek('like'):
        #    return self.consume('like').value
        else:
            return None

    
    def consume(self, expected_type):
        if len(self.tokens)>0:
            token = self.tokens.pop()
            if token.type == expected_type:
                #print("Consuming: ", token.type)
                return token
            else:
                raise RuntimeError(
                    "Expected token type {} but got {}\n".format(expected_type,
                                                                 token.type))

    def peek(self, expected_type, offset=0):
        return self.tokens[-1-offset].type == expected_type
