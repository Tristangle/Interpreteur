from test import printTreeGraph# à copier coller dans le script sinon
reserved = {
    'if' : 'IF',
    'while' : 'WHILE',
    'for' : 'FOR',
    'print' : 'PRINT',
    'def' : 'DEF'
    #'return' : 'RETURN'
}

tokens = [
             'NAME', 'NUMBER',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'COLON', 'AND', 'OR',
             'EQUAL', 'EQUALS', 'LOWER', 'HIGHER', 'LACCOL', 'RACCOL', 'COMMA', 'DPERIOD']+list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r';'
t_AND = r'\&'
t_OR = r'\|'
t_EQUALS = r'=='
t_LOWER = r'\<'
t_HIGHER = r'\>'
t_LACCOL = r'\{'
t_RACCOL = r'\}'
t_COMMA = r'\,'
t_DPERIOD = r'\:'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Ch  for reserved words
    return t




def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lexer = lex.lex()


# Parsing rules


def p_start(t):
    ''' start : linst'''
    t[0] = ('start', t[1])
    print(t[0])
    printTreeGraph(t[0])
    # eval(t[1])
    evalInst(t[1])


names= { }


def evalInst(t):
    print('evalInst', t)
    if t == 'empty' :return
    if type(t) != tuple:
        print('warning')
        return
    if t[0] == 'print':
        print('CALC>', evalExpr(t[1]))
    if t[0] == 'assign':
        names[t[1]]= evalExpr(t[2])
    if t[0] == 'bloc':
        evalInst(t[1])
        evalInst(t[2])
    if t[0] == 'IF' :
        if evalExpr(t[1])== True:
            evalInst(t[2])
    if t[0] == 'WHILE':
        if evalExpr(t[1]) == True:
            evalInst(t[1])
    if t[0] == 'FOR':
        if evalExpr(t[1]) == True:
            evalInst(t[2])




def evalExpr(t):
    print('eval de ', t)
    if type(t) is int: return t
    if type(t) is str: return names[t]
    if type(t) is tuple:
        if t[0] == '+': return evalExpr(t[1]) + evalExpr(t[2])
        if t[0] == '-': return evalExpr(t[1]) - evalExpr(t[2])
        if t[0] == '*': return evalExpr(t[1]) * evalExpr(t[2])
        if t[0] == '/': return evalExpr(t[1]) // evalExpr(t[2])
        if t[0] == '==': return evalExpr(t[1]) == evalExpr(t[2])

def p_line(t):
    '''linst : linst inst 
            | inst '''
    if len(t) == 3:
        t[0] = ('bloc', t[1], t[2])
    else:
        t[0] = ('bloc', t[1], 'empty')

def p_if(t):
    '''inst : IF LPAREN expression RPAREN LACCOL linst RACCOL'''
    t[0] = ('IF', t[3], t[6])

def p_while(t):
    '''inst : WHILE LPAREN expression RPAREN LACCOL linst RACCOL'''
    t[0] = ('WHILE', t[3], t[6])

def p_for(t):
    '''inst : FOR LPAREN inst expression COLON inst RPAREN LACCOL linst RACCOL'''
    t[0] = ('FOR', t[3], t[4], t[6], t[9])
def p_params(t):
    '''params :
              | NAME
              | params COMMA NAME'''
    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 4:
        t[0] = t[1] + [t[3]]
    else:
        t[0] = []

def p_void(t):
    '''inst : DEF NAME LPAREN params RPAREN DPERIOD linst COLON'''
    t[0] = ('DEF', t[2], t[4], t[7])

#def p_return(t):
#    '''return : RETURN expression'''
#    t[0] = ('return', t[2])

#def p_fonction(t):
#    '''inst : DEF NAME LPAREN params RPAREN DPERIOD linst return COLON'''
#    if len(t) == 10:
#        t[0] = ('DEF', t[2], t[4], t[7], t[8])
#    else:
#        t[0] = ('DEF', t[2], t[4], t[7], t[8])

def p_statement_assign(t):
    'inst : NAME EQUAL expression COLON'
    t[0] = ('assign', t[1], t[3])


def p_statement_print(t):
    'inst : PRINT LPAREN expression RPAREN COLON'
    t[0] = ('print', t[3])


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression OR expression
                  | expression AND expression
                  | expression EQUALS expression
                  | expression LOWER expression
                  | expression HIGHER expression
                  | expression DIVIDE expression'''
    t[0] = (t[2], t[1], t[3])


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_number(t):
    'expression : NUMBER'

    t[0] = t[1]


def p_expression_name(t):
    'expression : NAME'

    t[0] = t[1]


def p_error(t):
    print("Erreur de syntaxe : '%s'" % t.value)

import ply.yacc as yacc

parser = yacc.yacc()

# s='1+2;x=4 if ;x=x+1;'
s = 'def printest(a): print(a+1); printest();'


# with open("1.in") as file: # Use file to refer to the file object

# s = file.read()

parser.parse(s)

