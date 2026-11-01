def fatorial(n):
    if n == 0 or n ==1:
        return 1
    else:
        for i in range(1, n):
            n *= i
        return n
#print(fatorial(6))  # Output: 720

def visualizacaotorredehanoi(n: int):
    # Cria a origem com o maior disco (n) na base e o menor (1) no topo
    origem = list(range(n, 0, -1))  # [n, n-1, ..., 2, 1]
    trabalho = []
    destino = []
    
    print(f"Estado inicial: [{origem}, {trabalho}, {destino}]")
    
    # Função recursiva que recebe as referências das listas
    def torredehanoi(k, orig, dest, trab):
        if k > 0:
            # 1. Move k-1 discos da origem para o pino de trabalho
            torredehanoi(k-1, orig, trab, dest)
            
            # 2. Move o disco base da origem para o destino
            disco = orig.pop()
            dest.append(disco)
            print(f"Movimento: [{origem}, {trabalho}, {destino}]")
            
            # 3. Move os k-1 discos do pino de trabalho para o destino
            torredehanoi(k-1, trab, dest, orig)
            
    # Inicia a recursão
    torredehanoi(n, origem, destino, trabalho)
#visualizacaotorredehanoi(3)
def geradordelista(n:int):
    lista = []
    for i in range(1, n+1):
        lista.append(i)
    lista -= [72]
    return lista

#print(geradordelista(123))

def insercao(x:int, lista:list):
    if x in lista:
        return lista
    lista_aux = []
    inserido = False
    for i in lista:
        if x < i and not inserido:
            lista_aux.append(x)
            inserido = True
        lista_aux.append(i)
    if not inserido:
        lista_aux.append(x)
    return lista_aux

print(insercao(73, geradordelista(123)))