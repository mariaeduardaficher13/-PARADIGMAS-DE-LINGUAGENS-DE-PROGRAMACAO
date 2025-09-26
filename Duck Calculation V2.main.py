import re
from graphviz import Digraph

# Precedência e associatividade dos operadores
precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
associatividade = {'+': 'E', '-': 'E', '*': 'E', '/': 'E', '^': 'D'}

# Estrutura de nó da AST
class ASTNode:
    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita

# Tokenização da expressão
def tokenize(expr):
    expr = expr.replace(' ', '')
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isdigit() or expr[i] == '.':
            num = ''
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(num)
        elif expr[i] in '+-*/^()':
            if expr[i] == '-' and (i == 0 or expr[i-1] in '(^*/+-'):
                i += 1
                num = '-'
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                tokens.append(num)
            else:
                tokens.append(expr[i])
                i += 1
        else:
            raise ValueError(f"Caractere inválido: '{expr[i]}'")
    return tokens

# Validação de tokens
def validar_tokens(tokens):
    parens = 0
    prev = ''
    for token in tokens:
        if token == '(':
            parens += 1
        elif token == ')':
            parens -= 1
            if parens < 0:
                raise ValueError("Parênteses desbalanceados")
        elif token in '+-*/^':
            if prev in '+-*/^' or prev == '':
                raise ValueError("Operador inválido ou duplicado")
        prev = token
    if parens != 0:
        raise ValueError("Parênteses desbalanceados")

# Conversão para notação pós-fixa
def infixa_para_posfixa(tokens):
    pilha = []
    saida = []
    for token in tokens:
        if re.match(r'-?\d+(\.\d+)?', token):
            saida.append(token)
        elif token in precedencia:
            while (pilha and pilha[-1] in precedencia and
                   ((associatividade[token] == 'E' and precedencia[token] <= precedencia[pilha[-1]]) or
                    (associatividade[token] == 'D' and precedencia[token] < precedencia[pilha[-1]]))):
                saida.append(pilha.pop())
            pilha.append(token)
        elif token == '(':
            pilha.append(token)
        elif token == ')':
            while pilha and pilha[-1] != '(':
                saida.append(pilha.pop())
            if not pilha:
                raise ValueError("Parênteses desbalanceados")
            pilha.pop()
    while pilha:
        if pilha[-1] in '()':
            raise ValueError("Parênteses desbalanceados")
        saida.append(pilha.pop())
    return saida

# Construção da AST a partir da pós-fixa
def construir_ast(posfixa):
    pilha = []
    for token in posfixa:
        if re.match(r'-?\d+(\.\d+)?', token):
            pilha.append(ASTNode(token))
        else:
            direita = pilha.pop()
            esquerda = pilha.pop()
            pilha.append(ASTNode(token, esquerda, direita))
    return pilha[0] if pilha else None

# Desenho da AST com Graphviz
def desenhar_ast(node, nome_arquivo='ast'):
    dot = Digraph()
    contador = [0]

    def adicionar_nos(nodo):
        if nodo is None:
            return None
        id_atual = str(contador[0])
        dot.node(id_atual, nodo.valor)
        contador[0] += 1

        if nodo.esquerda:
            id_esq = adicionar_nos(nodo.esquerda)
            dot.edge(id_atual, id_esq)
        if nodo.direita:
            id_dir = adicionar_nos(nodo.direita)
            dot.edge(id_atual, id_dir)
        return id_atual

    adicionar_nos(node)
    dot.render(nome_arquivo, format='png', cleanup=True)

# Avaliação da expressão pós-fixa
def avaliar_posfixa(tokens):
    pilha = []
    for token in tokens:
        if re.match(r'-?\d+(\.\d+)?', token):
            pilha.append(float(token))
        else:
            if len(pilha) < 2:
                raise ValueError("Expressão mal formada")
            b = pilha.pop()
            a = pilha.pop()
            if token == '+':
                pilha.append(a + b)
            elif token == '-':
                pilha.append(a - b)
            elif token == '*':
                pilha.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Divisão por zero")
                pilha.append(a / b)
            elif token == '^':
                pilha.append(a ** b)
    if len(pilha) != 1:
        raise ValueError("Expressão mal formada")
    return pilha[0]

# Função principal de cálculo
def calcular(expressao):
    tokens = tokenize(expressao)
    validar_tokens(tokens)
    posfixa = infixa_para_posfixa(tokens)
    resultado = avaliar_posfixa(posfixa)
    ast = construir_ast(posfixa)
    desenhar_ast(ast, nome_arquivo='ast')
    return resultado

# Loop interativo 
if __name__ == "__main__":
    print("Duck Calculator")
    print("Digite 'sair' para encerrar.\n")

    while True:
        expr = input("Digite a expressão: ").strip()
        if expr.lower() == 'sair':
            print("Encerrando.")
            break
        try:
            resultado = calcular(expr)
            print("Resultado:", resultado)
            print("AST gerada como 'ast.png'\n")
        except Exception as e:
            print("Erro:", e)
            print()
