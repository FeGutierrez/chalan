from ftplib import error_reply
import ply.yacc as yacc

from .flex import tokens
from . import ast
var = {}

def p_id(p):
    """id : ID"""
    if var[p[1]]:
        p[0] = var[p[1]]
    else:
        p[0] = p[1]

def p_expression(p):
	"""code : expr
			| prog
			| functiondef
            | functioncall
            | code expr
			| code prog
			| code functiondef
            | id
            | access
			"""
	p[0] = p[1]

def p_expr(p):
    """expr : ID ASSIGN_T NUM
            | ID ASSIGN_T expr
            | ID ASSIGN_T vector
            | ID ASSIGN_T matrix
            | ID ASSIGN_T functioncall
            | NUM operator NUM
            | NUM operator expr
    """
    if (p[2] == '+'):
        p[0] = p[1] + p[3]
    elif (p[2] == '-'):
        p[0] = p[1] - p[3]
    elif (p[2] == '*'):
        p[0] = p[1] * p[3]
    elif (p[2] == '/'):
        p[0] = p[1] / p[3]
    elif (p[2] == '%'):
        p[0] = p[1] % p[3]
    elif (p[2] == '='):
        var[p[1]] = p[3]
        p[0] = var[p[1]]
    

def p_matrix(p):
    """matrix : matrix SEP OPENB vector CLOSEB
			| OPENB vector CLOSEB
            | matrix SEP OPENB vector_str CLOSEB
            | OPENB vector_str CLOSEB 
            | OPENB matrix CLOSEB"""
    if len(p) == 4:
        p[0] = [p[2]]
    else:
        p[0] = p[1]
        p[0].append(p[4])

def p_access(p):
    """access : ID OPENB NUM CLOSEB
    """
    idx = p[3]
    p[0] = var[p[1]][idx]
    

def p_vector(p):
    """vector : vector SEP NUM
		| NUM
        | OPENB vector CLOSEB
        | vector SEP vector
		vector_str : vector_str SEP ID
		| ID
        | OPENB vector_str CLOSEB
        | vector_str SEP vector_str
	"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_operator(p):
    """operator : MAS
                | MENOS
                | MULT
                | DIV
                | MODULO
                | ASSIGN_T
    """
    p[0] = p[1]

def p_prog(p):
    """prog : IF
    """
    p[0] = p[1]

def p_functiondef(p):
    """functiondef : IF
    """
    p[0] = p[1]

def p_functioncall(p):
    """functioncall : ID OPENP argumments CLOSEP
                    | customoperations OPENP argumments CLOSEP"""
    global var

    if p[1] in ast.functions.keys():
        p[3] = ast.functions[p[1]](p[3])
    
    
    p[0] = p[3]

def p_argumments(p):
    """argumments : argumments SEP ID
                  | argumments SEP NUM
                  | ID
                  | NUM
                  |
                """
    if len(p) == 2:
        if p[1] in var.keys():
            p[0] = [var[p[1]]]
        else:
            p[0] = [p[1]]
    
    elif len(p) == 1:
        p[0] = None
    
    else:
        if p[3] in var.keys(): 
            p[1].append([var[p[3]]])
        else:
            p[1].append(p[3])
        
        p[0] = p[1]

def p_customoperations(p):
    """customoperations : DOTOP
               | SEN
               | COS
               | TAN
               | ARCS
               | ARCO
               | ARCT
               | LOG"""
    p[0] = p[1]

def p_error(p):
	if p:
		print("Error sintáctico en '%s'" % p.value, p)
	else:
		print("Error sintáctico en EOF")

parser = yacc.yacc(debug=True, start='code')

def parse_string(s: str, display = True):
	try:
		result = parser.parse(s)
		if result is not None:
			if display:
				print("Code: ", s, '\nResult ->', result, end='\n\n')
			else:
				print(result)
	except Exception as e:
		print("Error en: ", s, '\n===>', e, end='\n\n')

if __name__ == '__main__':
	while True:
		try:
			s = input()
		except EOFError:
			break
		if not s: continue
		parse_string(s)

