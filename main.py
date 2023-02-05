import pygame
import sys
import random

"""CONFIGURAÇÔES"""
WIDTH = 720                     # tamanho da tela(quanto maior, mais lento)
HEIGHT = 480
ALG_RUN = 1                 # 1 = BFS      2 = DFS     3 = Bellman-Ford 
USE_RANDOM_COLOR = True
menu_x, menu_y = 720, 480
BLOCK_SIZE = 2                  # tamanho do block
ROWS = WIDTH // BLOCK_SIZE      # quantidade de linhas
COLUMNS = HEIGHT // BLOCK_SIZE
RANDOM_BFS = True               # muda o efeito de preenchimento da BFS
RANDOM_DFS = True
WATERMARK = True               # muda o efeito de preenchimento da DFS
TAXA_COR = 2                    # muda a frequencia com que cada cor é alterada, quanto maior, mais cores aparecerão (melhor efeito entre 16 e 100)
vertices = []
id_vertice = 0
RANDOM_BELLMAN_FORD = True
ALG = 'BFS'
RANDOM_SEARCH_ANSWER = 'Sim'
marcaDAgua = ''

'''CORES'''
RANDOM_COLOR = (random.randrange(256),random.randrange(256),random.randrange(256))
BLACK = (0, 0, 0)
BLUE = (20, 20, 255)
RED = (204, 20, 20)
GREEN = (20, 255, 20)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
CIAN = (52, 78, 91)

pygame.init()
display = pygame.display.set_mode((menu_x, menu_y))
clock = pygame.time.Clock()
pygame.display.set_caption("PixelArt")
pygame.mixer.music.load('assets/bgsong.mp3')
pygame.mixer.music.play(-1)

initial_art = pygame.image.load('assets/img/bfs_random_false.png').convert_alpha()
initial_art = pygame.transform.scale(initial_art,(menu_x, menu_y))

'''MENUS'''
def draw_text(text, font, color, scr, x, y):
  title = font.render(text, True, color)
  rect = title.get_rect(center=(x, y))
  scr.blit(title, rect)

def draw_resolution_menu():
  global WIDTH, HEIGHT
  pygame.display.update()
  passo = 10
  while True:
    display.fill(CIAN)
    font40 = pygame.font.Font('assets/title-font.ttf', 50)
    font20 = pygame.font.Font('assets/title-font.ttf', 20)
    font24 = pygame.font.Font('assets/title-font.ttf', 24)
    font_obs = pygame.font.Font('assets/title-font.ttf', 17)
    draw_text("Resolução:", font40, WHITE, display, 330, 55)
    
    draw_text("K/L Definir passo: ", font24, GREEN, display, 330, 155)
    draw_text(f"{passo}", font24, WHITE, display, 510, 155)
    draw_text("(K = -   L = +)", font_obs, RED, display, 330, 185)

    draw_text(",/. Largura: ", font24, GREEN, display, 280, 245)
    draw_text(f"{WIDTH}", font24, WHITE, display, 420, 245)
    draw_text("(, = -   . = +)", font_obs, RED, display, 280, 275)

    draw_text("X/C Altura: ", font24, GREEN, display, 280, 325)
    draw_text(f"{HEIGHT}", font24, WHITE, display, 420, 325)
    draw_text("(X = -   C = +)", font_obs, RED, display, 260, 355)

    draw_text("V - Voltar", font20, WHITE, display, 100, 440)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_v:
          draw_options_menu()
        if event.key == pygame.K_l:
            passo *= 10 if passo < 1000 else 1
            pygame.display.update()
        if event.key == pygame.K_k:
          passo //= 10 if passo > 1 else 1
          pygame.display.update()  
        if event.key == pygame.K_PERIOD:
          WIDTH += passo if WIDTH <= 5000 - passo else 0
          pygame.display.update()
        if event.key == pygame.K_COMMA:
          WIDTH -= passo if WIDTH > 24 + passo else 0
          pygame.display.update()
        if event.key == pygame.K_c:
          HEIGHT += passo if HEIGHT <= 5000 - passo else 0
          pygame.display.update()
        if event.key == pygame.K_x:
          HEIGHT -= passo if HEIGHT > 24 + passo else 0
          pygame.display.update()


    pygame.display.update()

def draw_options_menu():
  pygame.display.update()
  global BLOCK_SIZE, ALG_RUN, TAXA_COR, RANDOM_BFS, RANDOM_DFS, USE_RANDOM_COLOR, ROWS, COLUMNS, WATERMARK, RANDOM_BELLMAN_FORD, ALG, RANDOM_SEARCH_ANSWER
  b, d, s, n, f = "BFS", "DFS", "Sim", "Não", "Bellman-Ford"
  
  while True:
    
    display.fill(CIAN)
    font40 = pygame.font.Font('assets/title-font.ttf', 40)
    font20 = pygame.font.Font('assets/title-font.ttf', 16)
    font24 = pygame.font.Font('assets/title-font.ttf', 20)
    font_obs = pygame.font.Font('assets/title-font.ttf', 17)

    draw_text("Opções:", font40, WHITE, display, 330, 55)
    draw_text("K/L Tamanho do pixel:", font24, GREEN, display, 330, 115)
    draw_text(f"{BLOCK_SIZE}", font24, WHITE, display, 510, 115)
    draw_text("(K = -   L = +)", font_obs, RED, display, 330, 145)
    draw_text("B/D/F Algoritmo usado: ", font24, GREEN, display, 330, 185) #dúvida pelo terceiro algoritmo que tá entrando...
    draw_text(f"{ALG}", font24, WHITE, display, 580, 185)
    draw_text(",/. Taxa de mudança de cor: ", font24, GREEN, display, 330, 225)
    draw_text(f"{TAXA_COR}", font24, WHITE, display, 545, 225)
    draw_text("(, = -   . = +)", font_obs, RED, display, 330, 255)
    draw_text("S/N Usar busca aleatória:", font24, GREEN, display, 330, 285)
    draw_text(f"{RANDOM_SEARCH_ANSWER}", font24, WHITE, display, 560, 285)
    draw_text("(Melhores efeitos)", font_obs, RED, display, 330, 315)
    draw_text("G/H Usar cores aleatórias", font24, GREEN, display, 320, 355)
    draw_text(f"{s if USE_RANDOM_COLOR else n}", font24, WHITE, display, 560, 355)
    draw_text("(G = Não   H = Sim)", font_obs, RED, display, 330, 375)
    draw_text("W/E Deseja gerar a partir de uma marca d'água ?", font_obs, GREEN, display, 330, 400)
    draw_text(f"{s if WATERMARK else n}", font24, WHITE, display, 600, 400)
    draw_text("(W = Não   E = Sim)", font_obs, RED, display, 330, 425)
    draw_text("V - Voltar", font20, WHITE, display, 100, 440)
    draw_text("R - Resolução", font20, WHITE, display, 600, 440)
    
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_v:
          draw_main_menu()
        if event.key == pygame.K_r:
          draw_resolution_menu()
        if event.key == pygame.K_l:
          BLOCK_SIZE += 1 if BLOCK_SIZE < 40 else 0
          pygame.display.update()
        if event.key == pygame.K_k:
          BLOCK_SIZE -= 1 if BLOCK_SIZE > 1 else 0
          pygame.display.update()
        if event.key == pygame.K_b:
          ALG_RUN = 1
          ALG = 'BFS'
          pygame.display.update()
        if event.key == pygame.K_d:
          ALG_RUN = 2
          ALG = 'DFS'
          pygame.display.update()
        if event.key == pygame.K_f:
          ALG_RUN = 3
          ALG = 'BELLMAN-FORD'
          pygame.display.update()
        if event.key == pygame.K_PERIOD:
          TAXA_COR += 1
          pygame.display.update()
        if event.key == pygame.K_COMMA:
          TAXA_COR -= 1
          pygame.display.update()
        if event.key == pygame.K_s:
          if ALG_RUN == 1:
            RANDOM_DFS = True
            RANDOM_SEARCH_ANSWER = 'Sim'
            pygame.display.update()
          if ALG_RUN == 2:
            RANDOM_BFS = True
            RANDOM_SEARCH_ANSWER = 'Sim'
            pygame.display.update()
          if ALG_RUN == 3:
            RANDOM_BELLMAN_FORD = True
            RANDOM_SEARCH_ANSWER = 'Sim'
            pygame.display.update()
          pygame.display.update()
        if event.key == pygame.K_n:
          if ALG_RUN == 1:
            RANDOM_DFS = False
            RANDOM_SEARCH_ANSWER = 'Não'
            pygame.display.update()
          if ALG_RUN == 2:
            RANDOM_BFS = False
            RANDOM_SEARCH_ANSWER = 'Não'
            pygame.display.update()
          if ALG_RUN == 3:
            RANDOM_BELLMAN_FORD = False
            RANDOM_SEARCH_ANSWER = 'Não'
            pygame.display.update()
          pygame.display.update()
        if event.key == pygame.K_h:
          USE_RANDOM_COLOR = True
          pygame.display.update()
        if event.key == pygame.K_g:
          USE_RANDOM_COLOR = False
          pygame.display.update()
        if event.key == pygame.K_w:
          WATERMARK = False
          pygame.display.update()
          draw_start_menu()
        if event.key == pygame.K_e:
          WATERMARK = True
          pygame.display.update()
          watermark_input()
    
    ROWS = WIDTH // BLOCK_SIZE
    COLUMNS = HEIGHT // BLOCK_SIZE    
    pygame.display.update()
  
def draw_start_menu():
  pygame.display.update()
  display = pygame.display.set_mode((WIDTH, HEIGHT))
  fim_aug = True
  make_grid()
  FPS = 20
  while True:
    clock.tick(FPS)
    display.fill(CIAN)
    font40 = pygame.font.Font('assets/title-font.ttf', 30)
    font22 = pygame.font.Font('assets/title-font.ttf', 20)
    draw_text("Clique onde deseja iniciar.", font40, WHITE, display, 260, 50)
    draw_text("As vezes é necessário clicar mais de uma vez para começar.", font22, RED, display, 365, 80)
    draw_text("No fim aperte ESPAÇO para sair", font22, WHITE, display, 323, 440)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and fim_aug:
        fim_aug = False
        display.fill(CIAN)
        pos = pygame.mouse.get_pos()

        row = (pos[0]) // BLOCK_SIZE
        col = (pos[1]) // BLOCK_SIZE      
        
        if ALG_RUN == 1:
          bfs(vertices[int(row)][int(col)])
        if ALG_RUN == 2:
          dfs(vertices[int(row)][int(col)])
        if ALG_RUN == 1:
          bfs(vertices[int(row)][int(col)])
        if ALG_RUN == 3:
          bellman_ford(vertices[int(row)][int(col)])
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_p:
          screenshot = pygame.Surface((WIDTH, HEIGHT))
          screenshot.blit(display, (0, 0))
          pygame.image.save(screenshot, "print.png")
        if event.key == pygame.K_SPACE:
          fim_aug = True
          reset()
          draw_main_menu()
    if fim_aug:         
      pygame.display.update()

def draw_main_menu():
  pygame.display.update()
  display = pygame.display.set_mode((menu_x, menu_y))
  while True:
    display.blit(initial_art, (0,0))
    font80 = pygame.font.Font('assets/Championship.ttf', 80)
    font35 = pygame.font.Font('assets/Championship.ttf', 35)
    
    draw_text("PIXEL GRAPH ART", font80, WHITE, display, 360, 150)
    draw_text("CLIQUE NA TELA PARA INICIAR", font35, WHITE, display, 360, 260)
    draw_text("O - OPÇÕES", font35, WHITE, display, 150, 420)
    draw_text("S - SAIR", font35, WHITE, display, 590, 420)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_o:
          draw_options_menu()
        if event.key == pygame.K_s:
          pygame.quit()
          sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        draw_start_menu()

    pygame.display.update()

def watermark_input():
    pygame.display.update()
    global marcaDAgua
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    text_font = pygame.font.Font(None, 32)
    fim_aug = True
    make_grid()
    FPS = 20
    while True:
      clock.tick(FPS)
      display.fill(BLACK)
      font40 = pygame.font.Font('assets/Championship.ttf', 30)
      font22 = pygame.font.Font('assets/Championship.ttf', 20) 
      draw_text("DIGITE A MARCA D'ÁGUA: ", font22, WHITE, display, 150, 50)
      draw_text(marcaDAgua, font40, WHITE, display, 260, 150)
      draw_text("ENTER - CONFIRMAR", font22, WHITE, display, 150, 420)
      draw_text("SPACE - SAIR", font22, WHITE, display, 590, 420)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYUP:
          #if event.key == pygame.K_KP_ENTER:
            #screenshot = pygame.Surface((WIDTH, HEIGHT))
            #screenshot.blit(display, (0, 0))
            #pygame.image.save(screenshot, "print.png")
          if event.key == pygame.K_SPACE:
            fim_aug = True
            reset()
            draw_main_menu()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_BACKSPACE:
            marcaDAgua = marcaDAgua[:-1]
          else:
            marcaDAgua += event.unicode 
      if fim_aug:         
        pygame.display.update()
      text_surface = text_font.render(marcaDAgua,True,(255,255,255))
      display.blit(text_surface, (0,0))

class Vortex:
  def __init__(self, row, col, width, display, id) -> None:
    self.row = row * width
    self.col = col * width
    self.id = id
    self.x = row
    self.y = col
    self.color = WHITE
    self.width = width
    self.display = display
    self.neighbours = []
    self.is_vortex = True
    self.visited = False
    self.is_wall()

  def vortex(self, display, color=None):
    if color is None or not self.is_vortex:
      color = self.color
    else:
      self.color = color
    pygame.draw.rect(display, color, (self.row, self.col, self.width, self.width))
    pygame.display.update()

  def is_wall(self):
    w = self.display.get_width()
    h = self.display.get_height()
    y_cond = self.y == 0 or self.y >= h - 1
    x_cond = self.x == 0 or self.x >= w - 1

    if x_cond or y_cond:
      self.is_vortex = False
      self.color = BLACK
      self.neighbours = []

  def discover_neighbours(self, field):
    if (self.x > 0 and self.x < ROWS - 2) and (self.y > 0 and self.y < COLUMNS - 2):
      if field[self.x + 1][self.y].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y])     # vizinho da direita
      if field[self.x - 1][self.y].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y])     # vizinho da esquerda
      if field[self.x][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x][self.y + 1])     # vizinho de baixo
      if field[self.x][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x][self.y - 1])     # vizinho de cima
      if field[self.x - 1][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y - 1]) # superior esquerdo
      if field[self.x - 1][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y + 1]) # superior direito
      if field[self.x + 1][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y + 1]) # inferior direito
      if field[self.x + 1][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x + 1][self.y - 1]) # inferior esquerdo

def escolhe_cor(cor):
  nova_cor = list(cor)
  limite = 256

  if cor[0] > cor[1] and cor[0] > cor[2] and random.choice([True, False, False, False]): # elemento 0 é o maior da lista
    nova_cor[0] = (cor[0] + TAXA_COR) % limite
  if cor[1] > cor[0] and cor[1] > cor[2] and random.choice([True, False, False]): # elemento 1 é o maior da lista 
    nova_cor[1] = (cor[1] + TAXA_COR) % limite
  if cor[2] > cor[1] and cor[2] > cor[0] and random.choice([True, False]): # elemento 2 é o maior da lista 
    nova_cor[2] = (cor[2] + TAXA_COR) % limite
  else:
    i = random.randrange(0, 3)
    nova_cor[i] = (cor[i] + TAXA_COR) % limite

  return tuple(nova_cor)

def make_grid():
  global vertices, id_vertice

  vertices = []
  for i in range(ROWS):
    cols = []
    for j in range(COLUMNS):
      cols.append(Vortex(i, j, WIDTH // ROWS, display, id_vertice // BLOCK_SIZE))
      id_vertice += BLOCK_SIZE
    vertices.append(cols)

  for i in range(ROWS):
    for j in range(COLUMNS):
      vertices[i][j].discover_neighbours(vertices)

def bfs(node):
  queue = []
  global RANDOM_COLOR
  node.visited = True
  node.vortex(display, color=RANDOM_COLOR)
  queue.append(node)
  
  while queue:
    s = random.choice(queue) if RANDOM_BFS else queue.pop(0)
    queue.pop(queue.index(s)) if RANDOM_BFS else None

    for n in s.neighbours:
      if not n.visited:
        n.visited = True
        queue.append(n)
        cor = escolhe_cor(s.color)
        RANDOM_COLOR = (random.randrange(256),random.randrange(256),random.randrange(256))
        n.vortex(display, color=cor if not USE_RANDOM_COLOR else RANDOM_COLOR)

def dfs(node):
  stack = [node]

  while stack:
    s = stack.pop()

    if s.visited:
      continue
    s.visited = True
    for n in s.neighbours:
      stack.append(random.choice(s.neighbours) if RANDOM_DFS else n)
      cor = escolhe_cor(s.color)
      RANDOM_COLOR = (random.randrange(256),random.randrange(256),random.randrange(256))
      n.vortex(display, color=cor if not USE_RANDOM_COLOR else RANDOM_COLOR)

def bellman_ford(node):
  graph_len = len(vertices)
  distancia = [float('inf') for _ in range(graph_len ** 2)]
  distancia[node.id] = 0

  for _ in range(graph_len - 1):
    for source in node.neighbours:
      destiny = random.choice(source.neighbours)
      if distancia[source.id] != float("inf") and distancia[source.id] + 1 < distancia[destiny.id]:
        distancia[destiny.id] = distancia[source.id] + 1
        cor = escolhe_cor(source.color)
        RANDOM_COLOR = (random.randrange(256),random.randrange(256),random.randrange(256))
        source.vortex(display, color=cor if not USE_RANDOM_COLOR else RANDOM_COLOR)

  for source in node.neightoubrs:
    destiny = random.choice(node.neighbours)
    if distancia[source.id] != float("inf") and distancia[source.id] + 1 < distancia[destiny.id]:
      return


def reset():
  for i in range(ROWS):
    for j in range(COLUMNS):
      vertices[i][j].visited = False



if __name__ == '__main__':
  
  draw_main_menu()
