import random
from collections import deque

# Constantes do Labirinto
TAMANHO = 10              # Tamanho do labirinto (10x10)
OBSTACULOS_MIN = 15       # Quantidade mínima de obstáculos
OBSTACULOS_MAX = 35       # Quantidade máxima de obstáculos
ENERGIA_INICIAL = 50      # Energia inicial do agente

def gerar_labirinto():
    # Cria a matriz 10x10
    labirinto = [['.' for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    
    # Gera uma quantidade aleatória de obstáculos
    num_obstaculos = random.randint(OBSTACULOS_MIN, OBSTACULOS_MAX)
    for _ in range(num_obstaculos):
        while True:
            i = random.randint(0, TAMANHO-1)
            j = random.randint(0, TAMANHO-1)
            # Garante que não bloqueie o ponto de início ou fim
            if (i, j) not in [(0, 0), (9, 9)] and labirinto[i][j] == '.':
                labirinto[i][j] = '#'  # Define obstáculo
                break

    # Posiciona 5 bônus de energia (+5 de energia)
    for _ in range(5):
        while True:
            i = random.randint(0, TAMANHO-1)
            j = random.randint(0, TAMANHO-1)
            if labirinto[i][j] == '.':
                labirinto[i][j] = '+'
                break

    # Posiciona 3 bônus de energia maiores (+10 de energia)
    for _ in range(3):
        while True:
            i = random.randint(0, TAMANHO-1)
            j = random.randint(0, TAMANHO-1)
            if labirinto[i][j] == '.':
                labirinto[i][j] = '*'
                break

    # Define os pontos de início e fim
    labirinto[0][0] = 'S' 
    labirinto[9][9] = 'E'
    return labirinto

# Função para exibir o labirinto de forma visual no terminal
def mostrar_labirinto(lab):
    print("+" + "---+" * TAMANHO)
    for linha in lab:
        print("|", end='')
        for celula in linha:
            if celula == '#':
                print("###|", end='')   # Obstáculo
            elif celula == '+':
                print(" + |", end='')   # Bônus de energia +5
            elif celula == '*':
                print(" * |", end='')   # Bônus de energia +10
            elif celula == 'S':
                print(" S |", end='')   # Início
            elif celula == 'E':
                print(" E |", end='')   # Fim
            elif celula == 'o':
                print(" o |", end='')   # Caminho percorrido
            else:
                print("   |", end='')   # Espaço livre
        print()
        print("+" + "---+" * TAMANHO)

# Função que realiza a busca com controle de energia
def busca(lab):
    fila = deque() 
    visitados = set()  
    fila.append(((0, 0), [], ENERGIA_INICIAL)) 

    while fila:
        (i, j), caminho, energia = fila.popleft()

        # Se energia acabou, não continua
        if energia <= 0:
            continue

        # Se chegou no destino, retorna o caminho e a energia restante
        if (i, j) == (9, 9):
            return caminho + [(i, j)], energia

        # Ignora se já visitou
        if (i, j) in visitados:
            continue
        visitados.add((i, j))

        # Atualiza energia
        nova_energia = energia - 1 
        if lab[i][j] == '+':
            nova_energia += 5       
        elif lab[i][j] == '*':
            nova_energia += 10      

        # Explora as 4 direções (cima, baixo, esquerda, direita)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < TAMANHO and 0 <= nj < TAMANHO:
                if lab[ni][nj] != '#':  # Não vai para obstáculo
                    fila.append(((ni, nj), caminho + [(i, j)], nova_energia))

    # Se não encontrar caminho, retorna None
    return None, 0

# Execução principal
lab = gerar_labirinto()  
print("Labirinto Inicial:")
mostrar_labirinto(lab)   

caminho, energia_final = busca(lab)

# Se caminho encontrado, marca no labirinto e exibe resultado
if caminho:
    print("Caminho encontrado!")
    for i, j in caminho:
        if lab[i][j] == '.':
            lab[i][j] = 'o'  # Marca caminho
    mostrar_labirinto(lab)
    print(f"Energia restante: {energia_final}")
else:
    print("Caminho não encontrado ou energia insuficiente.")
