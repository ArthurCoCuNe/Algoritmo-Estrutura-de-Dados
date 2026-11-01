import EstruturasDeDados.Data_Structures.Stack.stack as stack

def infixaparaposfixa(expressao_infixa: str):
    pilha = stack.Stack()
    pilha_oprs = stack.Stack()
    operadores = '+-*/^$'
    parenteses = '()'
    for i in range(len(expressao_infixa)):
        if expressao_infixa[i] not in operadores and expressao_infixa[i] not in parenteses:
            pilha.push(expressao_infixa[i])
        if expressao_infixa[i] == '(':
            pilha_oprs.push(expressao_infixa[i])
        if expressao_infixa[i] == ')':
            op1 = pilha.peek()
            pilha.pop()
            op2 = pilha.peek()
            pilha.pop()
            pilha.push(op1 + op2 + expressao_infixa[i-1])
        if expressao_infixa[i] in operadores:
            while not pilha_oprs.is_empty() and pilha_oprs.peek() != '(' and precedencia(expressao_infixa[i], pilha_oprs.peek()):
                op1 = pilha.peek()
                pilha.pop()
                op2 = pilha.peek()
                pilha.pop()
                pilha.push(op1 + op2 + pilha_oprs.peek())
                pilha_oprs.pop()
            pilha_oprs.push(expressao_infixa[i])
    while not pilha_oprs.is_empty():
        op1 = pilha.peek()
        pilha.pop()
        op2 = pilha.peek()
        pilha.pop()
        pilha.push(op1 + op2 + pilha_oprs.peek())
        pilha_oprs.pop()
    return pilha.peek()

print(infixaparaposfixa("A+B*C-(D/E-F)")) # expected output: "ABC*+DE/F-"

def infixaparaprefixa(expressao_infixa: str):
    pass

def posfixaparainfixa(expressao_posfixa: str):
    pass

def prefixaparainfixa(expressao_prefixa: str):
    pass

def posfixaparaprefixa(expressao_posfixa: str):
    pilha = stack.Stack()
    operadores = '+-*/^$'
    for i in range(len(expressao_posfixa)):
        if expressao_posfixa[i] not in operadores:
            pilha.push(expressao_posfixa[i])

        if expressao_posfixa[i] in operadores:
            op2 = pilha.peek()
            pilha.pop()
            op1 = pilha.peek()
            pilha.pop()
            pilha.push(expressao_posfixa[i] + op1 + op2)
    return pilha.peek()

#print(posfixaparaprefixa("ABC/-DEF/-*")) # expected output: "*-A/BC-/DEF"]

def prefixaparaposfixa(expressao_prefixa: str):
    pilha = stack.Stack()
    operadores = '+-*/^$'
    for i in range(len(expressao_prefixa)-1, -1, -1):
        if expressao_prefixa[i] not in operadores:
            pilha.push(expressao_prefixa[i])

        if expressao_prefixa[i] in operadores:
            op1 = pilha.peek()
            pilha.pop()
            op2 = pilha.peek()
            pilha.pop()
            pilha.push(op1 + op2 + expressao_prefixa[i])
    return pilha.peek()

#print(prefixaparaposfixa("*-A/BC-/DEF")) # expected output: "ABC/-DEF/-*"]

def precedencia(opr1: str, opr2: str):
    def peso(operador: str):
        if operador == '+' or operador == '-':
            return 1
        elif operador == '*' or operador == '/':
            return 2
        elif operador == '^' or operador == '$':
            return 3
        else:
            return 0
    diff = peso(opr1) - peso(opr2)
    if (opr1 == '$' or opr1 == '^') and (opr2 == '$' or opr2 == '^'):
        return False
    if diff >= 0:
        return True
    else:
        return False