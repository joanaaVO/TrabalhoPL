import ply.yacc as yacc
import sys

from conversor_lex import tokens
from conversor_lex import literals
from conversor_lex import states

def p_programa(p):
    'programa : lex yacc'
    p[0] = p[1] + p[2] 
    parser.output += p[0]

def p_lex(p):
    'lex : LEX vars FUNCTIONS funcs'
    p[0] = "import ply.lex as lex\n\n" + p[2] + "\n" + p[4] + "lexer = lex.lex()\n\n\n"
 
def p_yacc(p):
    'yacc : YACC vars ERS ers PYTHON python vars PYTHON python END'
    p[0] = "import ply.yacc as yacc\n\n" + p[2] + "\n" + p[4] + p[6] + p[7] + "\n" + p[9]  

def p_vars_var(p):
    'vars : vars comment var vcomment'
    p[0] = p[1] + p[2] + p[3] + " " + p[4]
    
def p_vars_empty(p):
    'vars : '
    p[0] = ''

def p_var_number(p):
    "var : PERC ID '=' NUM"
    p[0] = p[2] + ' = ' + p[4]

def p_var_regex(p):
    "var : PERC ID '=' REGEX"
    p[0] = f"t_{p[2]}" + ' = ' + p[4]

def p_var_string(p):
    "var : PERC ID '=' STRING"
    if p[2] == "ignore":
        p[0] = f"t_{p[2]}" + ' = ' + p[4]
    else : 
        p[0] = p[2] + ' = ' + p[4]    

def p_var_yacc(p):
    "var : PERC ID '=' YACC"
    p[0] = "\n" + p[2] + ' = ' + "yacc." + p[4] + "\n"

def p_var_lista(p):
    "var : PERC ID '=' LIST"
    p[0] = p[2] + ' = ' + p[4]

def p_var_emptylista(p):
    "var : PERC ID '=' EMPTYLIST"
    p[0] = p[2] + ' = ' + p[4] 

def p_funcs_list(p):
    'funcs : funcs comment func'
    p[0] = p[1] + p[2] + p[3] + "\n"

def p_funcs_empty(p):
    'funcs : '
    p[0] = ''

def p_func_ret(p):
    "func : ER RETURN PAL PAL"
    p[0] = "def " + "t_" + p[3] + "(t):" + "\n\t" + f"r'{p[1]}'\n\t" + f"t.value = {p[4]}\n\t" + f"{p[2]} t\n"

def p_func_errorf(p):
    "func : PONTO ERROR PAL STRING PAL"
    p[0] = "def t_error(t):\n\t" + f"print({p[3]}{p[4]})\n\t" + p[5] + "\n" 

def p_func_error(p):
    "func : PONTO ERROR STRING PAL"
    p[0] = "def t_error(t):\n\t" + f"print({p[2]})\n\t" + p[3] + "\n"  

def p_func_end(p):
    'func : END'
    p[0] = '' 

def p_python_list(p):
    "python : python TEXT"
    p[0] = p[1] + p[2] + "\n"    

def p_python_empty(p):
    "python : "
    p[0] = ''

def p_ers_empty(p):
    "ers : "
    p[0] = ''

def p_ers_list(p):
    "ers : ers comment er"
    p[0] = p[1] + p[2] + p[3] + "\n"

def p_er(p):
    "er : EXP STRING EXP"
    var = p[1][:-1]
    if var in p.parser.erfunc:
        p.parser.erfunc[var] += 1
        p[1] = var + f'_{p.parser.erfunc[var]}'
    else:
        p.parser.erfunc[var] = 1
        p[1] = var + f'_{p.parser.erfunc[var]}'

    p[0] = f"def p_{p[1]}(t):\n\t" + f"\"{var} : {p[2][1:]}\n\t{p[3]}\n"

def p_vcomment_com(p):
    "vcomment : VCOMMENT"
    p[0] = p[1] + "\n"

def p_vcomment_empty(p):
    "vcomment : "
    p[0] = "\n"  

def p_comment_com(p):
    "comment : COMMENT"
    p[0] = p[1] + "\n"

def p_comment_empty(p):
    "comment : "
    p[0] = '' 

def p_error(p):
    print(f"Erro sintático! em {p.value}")


parser = yacc.yacc()
parser.output = ""
parser.erfunc = {}

def main():
    if len(sys.argv) == 1: file = "sintaxe.txt"
    elif len(sys.argv) > 2: 
        raise NameError("Argumentos a mais na funcao principal\n")
    else: file = sys.argv[1]

    f = open(file)
    content = f.read()
    result = parser.parse(content)
    f.close()
    f = open(file[:-4] + ".py", 'w')
    f.write(parser.output)
    f.close()

main()    