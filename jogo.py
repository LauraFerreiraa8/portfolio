import pygame
import random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIGURAÇÕES ---
WIDTH, HEIGHT = 800, 500
ASSETS_DIR = resource_path('assets')
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Panetteria Gethsemane Express")
clock = pygame.time.Clock()
font_msg = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 18, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

def load_img(name, size, transparent=True):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            if transparent: img.set_colorkey(WHITE)
            return pygame.transform.scale(img, size)
        except: return None
    return None

# Imagens com tamanhos aumentados
img_fundo = load_img("fundo.png", (WIDTH, HEIGHT), False)
img_p = load_img("boneco.png", (120, 120)) # Aumentado
img_obs = load_img("caixa.png", (100, 100)) # Aumentado

ranking = []

def get_player_name():
    name = ""
    input_active = True
    while input_active:
        screen.fill((30, 30, 30))
        # Instruções claras
        instr1 = font_small.render("COMO JOGAR: Use SETAS (Cima/Baixo) ou W/S para desviar das caixas.", True, WHITE)
        instr2 = font_small.render("OBJETIVO: Sobreviva o maior tempo possível para pontuar!", True, WHITE)
        prompt = font_msg.render("DIGITE SEU NOME E APERTE ENTER:", True, GOLD)
        name_img = font_msg.render(name, True, WHITE)
        
        screen.blit(instr1, (WIDTH//2 - instr1.get_width()//2, 50))
        screen.blit(instr2, (WIDTH//2 - instr2.get_width()//2, 80))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 40))
        screen.blit(name_img, (WIDTH//2 - name_img.get_width()//2, HEIGHT//2 + 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() != "": input_active = False
                elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                else: 
                    if len(name) < 12: name += event.unicode
        pygame.display.flip()
    return name

class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.x = WIDTH + 100
        self.y = [250, 340, 430][lane] # Ajuste de altura para imagens maiores
        self.rect = pygame.Rect(self.x + 10, self.y - 40, 80, 80) # Hitbox ajustada
    def update(self, speed):
        self.x -= speed
        self.rect.x = self.x
    def draw(self):
        if img_obs: screen.blit(img_obs, (self.x, self.y - 50))
        else: pygame.draw.rect(screen, (200, 0, 0), self.rect)

def play_game(player_name):
    lanes_y = [250, 340, 430]
    player_lane = 1
    player_y = lanes_y[player_lane]
    player_x = 150
    score, lives = 0, 3
    entities = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 0
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w] and player_lane > 0: player_lane -= 1
                if event.key in [pygame.K_DOWN, pygame.K_s] and player_lane < 2: player_lane += 1

        score += 1
        speed = 6 + (score / 800)
        player_y += (lanes_y[player_lane] - player_y) * 0.15

        if random.random() < 0.02: entities.append(Obstacle(random.randint(0, 2)))

        for obs in entities[:]:
            obs.update(speed)
            p_rect = pygame.Rect(player_x - 30, player_y - 40, 60, 80) # Hitbox do boneco
            if p_rect.colliderect(obs.rect):
                lives -= 1
                entities.remove(obs)
                if lives <= 0: return score // 10
            if obs.x < -150: entities.remove(obs)

        if img_fundo: screen.blit(img_fundo, (0, 0))
        else: screen.fill((18, 68, 126))
        
        for obs in entities: obs.draw()
        if img_p: screen.blit(img_p, (player_x - 60, player_y - 60))
        
        s_txt = font_small.render(f"PLAYER: {player_name} | PONTOS: {score // 10} | VIDAS: {lives}", True, WHITE)
        screen.blit(s_txt, (20, 20))
        pygame.display.flip()
        clock.tick(60)

while True:
    current_name = get_player_name()
    final_score = play_game(current_name)
    ranking.append((current_name, final_score))
    ranking = sorted(ranking, key=lambda x: x[1], reverse=True)[:15] # Top 15
    
    show_rank = True
    while show_rank:
        screen.fill((15, 15, 15))
        title = font_msg.render("RANKING - TOP 15", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        for i, (name, pts) in enumerate(ranking):
            col = i // 8  # Divide em duas colunas se necessário
            row = i % 8
            line = font_small.render(f"{i+1:02d}. {name:12s} : {pts} pts", True, WHITE)
            screen.blit(line, (150 + col*300, 80 + row*40))
        
        msg = font_small.render("ESPAÇO para Novo Jogo | ESC para Sair", True, GOLD)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: show_rank = False
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()