#!/usr/bin/env python
# TOKENIZER

import re 


class Tokenizer(object):
    """docstring for Tokenizer"""

    def __init__(self, code):
        super(Tokenizer, self).__init__()
        self.code = code

        self.TOKENS_TYPE = [['comment', r'\/\*(?:(?!\*\/).)*\*\/'],
                            ['let', r'\%\b(LET)\b'],
                            ['proc', r'\bPROC\b'],
                            ['freq', r'\bFREQ\b'],
                            ['sort', r'\bSORT\b'],
                            ['title', r'\bTITLE\b'],
                            ['data', r'\bDATA\b'],
                            ['set', r'\bSET\b'],
                            ['if', r'\bIF\b'],
                            ['elseif', r'\bELSE IF\b'],
                            ['else', r'\bELSE\b'],
                            ['end', r'\bEND\b'],
                            ['run', r'\bRUN\b'],
                            ['and', r'\bAND\b'],
                            ['or', r'\bOR\b'],
                            ['then', r'\bTHEN\b'],
                            ['do', r'\bDO\b'],
                            ['in', r'\bIN\b'],
                            ['where', r'\bWHERE\b'],
                            ['eq', r'(\bEQ\b|\=)'],
                            ['macrovar', r'\&[a-zA-Z0-9]+\.'],
                            ['string', r'([\'][^\']*[\']|[\"][^\"]*[\"])'],
                            ['integer', r'\b\d+\b'],
                            ['float', r'\b\d+\.\d+\b'],
                            ['identifier', r'[a-zA-Z0-9\_\.]+'],
                            ['comma', r'\,'],
                            ['oparen', r'\('],
                            ['cparen', r'\)'],
                            ['ge', r'\>='],
                            ['le', r'\<='],
                            ['lt', r'\<'],
                            ['gt', r'\>'],
                            ['plus', r'\+'],
                            ['minus', r'\-'],
                            ['multiply', r'\*'],
                            ['division', r'\/'],
                            ['semicolon', r';']]

    def tokenize(self):
        tokens = []
        while len(self.code) > 0:
            tokens.append(self.tokenize_one_token())
            self.code = self.code.strip()
        tokens.reverse()
        return tokens

    def tokenize_one_token(self):
        try:
            for type, regex in self.TOKENS_TYPE:
                match = re.search(r'\A({})'.format(regex),
                                  self.code, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    self.code = self.code[len(value):]
                    return Token(type, value)
            raise RuntimeError(
                "Couldn't match token on \n{}".format(self.code))
        except RuntimeError as e:
            print("ERROR: " + str(e))
            raise


class Token:
    """docstring for Token"""

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return '<class Token type=%s, value=\"%s\" \n' % (self.type, self.value)
