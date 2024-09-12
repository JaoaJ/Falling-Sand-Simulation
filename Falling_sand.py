import pygame
import sys

# Definições de largura, altura e outros parâmetros
WIDTH = 500
HEIGHT = 900
TAMANHO_PIXEL = 10
FPS = 40

# Invertendo corretamente as dimensões do grid
LINHAS = HEIGHT // TAMANHO_PIXEL
COLUNAS = WIDTH // TAMANHO_PIXEL

# Inicialização do pygame
pygame.init()

tela = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Função para criar a matriz (grid)
def criar_matriz(linhas, colunas):
    matriz = []
    for i in range(linhas):
        linha = [0] * colunas
        matriz.append(linha)
    return matriz

# Criação do grid inicial
GRID = criar_matriz(linhas=LINHAS, colunas=COLUNAS)

# Função para desenhar o grid na tela
def desenhar_grid(TAMANHO_PIXEL, WIDTH, HEIGHT, GRID):
    for x in range(0, WIDTH, TAMANHO_PIXEL):
        for y in range(0, HEIGHT, TAMANHO_PIXEL):
            retangulo = pygame.Rect(x, y, TAMANHO_PIXEL, TAMANHO_PIXEL)
            pygame.draw.rect(tela, (0, 0, 0), retangulo, 1)
            if GRID[y // TAMANHO_PIXEL][x // TAMANHO_PIXEL] == 1:
                pygame.draw.rect(tela, (255, 128, 13), retangulo)  # Cor laranja
            elif GRID[y // TAMANHO_PIXEL][x // TAMANHO_PIXEL] == 2:
                pygame.draw.rect(tela, (162, 25, 255), retangulo)  # Cor roxa

# Função para atualizar o grid e mover os pixels
def atualizar_grid(GRID):
    for row in range(len(GRID) - 2, -1, -1):  # Começar a verificação da segunda linha de baixo para cima
        for col in range(len(GRID[row])):
            if GRID[row][col] in [1, 2]:  # Se o pixel for 1 ou 2
                # Tenta cair diretamente para baixo
                if GRID[row + 1][col] == 0:
                    GRID[row + 1][col] = GRID[row][col]
                    GRID[row][col] = 0
                # Se não puder cair diretamente para baixo, tenta diagonal esquerda ou direita
                elif col > 0 and GRID[row + 1][col - 1] == 0:  # Diagonal esquerda
                    GRID[row + 1][col - 1] = GRID[row][col]
                    GRID[row][col] = 0
                elif col < len(GRID[row]) - 1 and GRID[row + 1][col + 1] == 0:  # Diagonal direita
                    GRID[row + 1][col + 1] = GRID[row][col]
                    GRID[row][col] = 0

# Loop principal do jogo
while True:
    tela.fill((0, 0, 0))  # Limpa a tela preenchendo com a cor de fundo
    desenhar_grid(TAMANHO_PIXEL=TAMANHO_PIXEL, WIDTH=WIDTH, HEIGHT=HEIGHT, GRID=GRID)
    atualizar_grid(GRID)

    # Tratamento de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Verifica o estado do mouse (clique esquerdo ou direito) e se ele está dentro da janela
    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x < WIDTH and 0 <= mouse_y < HEIGHT:  # Verifica se o mouse está dentro da janela
            col, row = mouse_x // TAMANHO_PIXEL, mouse_y // TAMANHO_PIXEL
            if row < LINHAS - 2 and col < COLUNAS - 2:  # Garantir que esteja dentro dos limites
                if pygame.mouse.get_pressed()[0]:  # Clique esquerdo (adiciona pixels laranjas)
                    GRID[row][col] = 1
                    GRID[row + 1][col] = 1
                    GRID[row][col + 1] = 1
                    GRID[row + 1][col + 1] = 1
                elif pygame.mouse.get_pressed()[2]:  # Clique direito (adiciona pixels roxos)
                    GRID[row][col] = 2
                    GRID[row + 1][col] = 2
                    GRID[row][col + 1] = 2
                    GRID[row + 1][col + 1] = 2

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(FPS)
