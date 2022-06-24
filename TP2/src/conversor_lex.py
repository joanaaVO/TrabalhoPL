import re
import ply.lex as lex
from urllib3 import Retry

tokens = ['LEX', 'YACC', 'FUNCTIONS', 'ERS', 
        "COMMENT", 'ID', 'STRING', 'PERC', "ER", 
        "RETURN", "PAL", "ERROR", "LIST", "END", 
        "EMPTYLIST", "EXP", "TEXT", "PYTHON", 
        "PONTO", "VCOMMENT", "NUM", "REGEX"]

literals = ['=']

states = [("var", "exclusive"), ("func", "exclusive"), ("er", "exclusive"), ("python", "exclusive")]

def t_LEX(t):
    r'%%\sLEX'
    return t

def t_YACC(t):
    r'%%\sYACC'
    return t

def t_PYTHON(t):
    r'%%\sPYTHON'
    t.lexer.begin("python")
    return t 

def t_FUNCTIONS(t):
    r'%%\sFUNCTIONS'
    t.lexer.begin("func")
    return t

def t_ERS(t):
    r'%%\sERS'
    t.lexer.begin("er")
    return t

def t_VCOMMENT(t):
    r'\#{2}.*'
    return t

def t_COMMENT(t):
    r'\#.*'
    return t

def t_func_COMMENT(t):
    r'\#.*'
    return t    

def t_PERC(t):
    r'%'
    t.lexer.begin("var")
    return t

def t_var_REGEX(t):
    r'r\'.*\''
    t.lexer.begin("INITIAL")
    return t   

def t_var_NUM(t):
    r'[0-9]+'
    t.lexer.begin("INITIAL")
    return t  

def t_var_YACC(t):
    r'yacc\(\)'
    t.lexer.begin("INITIAL")
    return t      

def t_var_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_\.]*'
    return t        

def t_var_STRING(t):
    r'\".*\"'
    t.lexer.begin("INITIAL")
    return t
    
def t_var_LIST(t):
    r'\[.*\]'
    t.lexer.begin("INITIAL")
    return t

def t_var_EMPTYLIST(t):
    r'\{\}'
    t.lexer.begin("INITIAL")
    return t   
  
def t_func_RETURN(t):
    r'return'
    return t

def t_func_ERROR(t):
    r'error'
    return t

def t_func_YACC(t):
    r'%%\sYACC'
    t.lexer.begin("INITIAL")
    return t

def t_func_STRING(t):
    r'\".*\"'
    return t

def t_func_PONTO(t):
    r'\.'
    return t

def t_func_PAL(t):
    r'[a-zA-Z0-9\.\(\)]+'
    return t

def t_func_ER(t): 
    r'[^\s]+'
    return t

def t_er_STRING(t):
    r'\".*\"'
    return t

def t_er_PYTHON(t):
    r'%%\sPYTHON'
    t.lexer.begin("python")
    return t 

def t_er_EXP(t):
    r'[^\}\"\:]+'
    return t

def t_python_END(t):
    r'%%'
    t.lexer.begin("INITIAL")
    return t

def t_python_PERC(t):
    r'%'
    t.lexer.begin("var")
    return t

def t_python_TEXT(t):
    r'.+'
    return t    

t_ignore = " \t\n\r"
t_var_ignore = " \t\n\r"
t_func_ignore = " \t\n\r,'()"
t_er_ignore = " \t\n\r}{:"
t_python_ignore = "\n\t\r"

def t_var_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer.skip(1)

def t_func_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer.skip(1) 

def t_er_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer.skip(1) 

def t_python_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer.skip(1) 

def t_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

