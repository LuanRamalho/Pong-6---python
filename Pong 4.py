import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_COLOR = (34, 139, 34)  # Verde

# Configurações do jogo
FPS = 60
BALL_RADIUS = 10
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
WHITE = (255, 255, 255)
FONT_COLOR = WHITE
LINE_COLOR = WHITE

# Configurações de velocidade
BALL_SPEED_X = 8
BALL_SPEED_Y = 8
PADDLE_SPEED = 6

# Configurações da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
font = pygame.font.Font(None, 50)

# Função para desenhar o fundo
def draw_background():
    screen.fill(SCREEN_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 4)
    pygame.draw.circle(screen, LINE_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 4)

# Função principal do jogo
def pong_game(multiplayer=False):
    # Inicialização dos objetos do jogo
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    player1 = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    player2 = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    player1_speed = 0
    player2_speed = 0

    player1_score = 0
    player2_score = 0

    clock = pygame.time.Clock()
    running = True

    # Cronômetro do jogo (2 minutos em segundos)
    game_time = 2 * 60

    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1_speed = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    player1_speed = PADDLE_SPEED
                if multiplayer:
                    if event.key == pygame.K_UP:
                        player2_speed = -PADDLE_SPEED
                    if event.key == pygame.K_DOWN:
                        player2_speed = PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1_speed = 0
                if multiplayer:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2_speed = 0

        # Atualização das posições
        player1.y += player1_speed
        if multiplayer:
            player2.y += player2_speed
        else:
            # Movimento automático do jogador 2 (IA)
            if ball.centery > player2.centery:
                player2.y += PADDLE_SPEED
            if ball.centery < player2.centery:
                player2.y -= PADDLE_SPEED

        # Restrições das paletas
        player1.y = max(0, min(player1.y, SCREEN_HEIGHT - PADDLE_HEIGHT))
        player2.y = max(0, min(player2.y, SCREEN_HEIGHT - PADDLE_HEIGHT))

        # Movimento da bola
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Colisões com as bordas
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1
        if ball.left <= 0:
            player2_score += 1
            ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
            ball_speed_x *= -1
        if ball.right >= SCREEN_WIDTH:
            player1_score += 1
            ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
            ball_speed_x *= -1

        # Colisões com as paletas
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        # Desenho na tela
        draw_background()
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        # Placar
        player1_text = font.render(str(player1_score), True, FONT_COLOR)
        player2_text = font.render(str(player2_score), True, FONT_COLOR)
        screen.blit(player1_text, (SCREEN_WIDTH // 4, 20))
        screen.blit(player2_text, (SCREEN_WIDTH * 3 // 4, 20))

        # Cronômetro
        game_time -= 1 / FPS
        minutes = int(game_time) // 60
        seconds = int(game_time) % 60
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, FONT_COLOR)
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(FPS)

        # Verificar se o tempo acabou
        if game_time <= 0:
            running = False

    # Exibir o resultado final
    screen.fill(SCREEN_COLOR)
    if player1_score > player2_score:
        result_text = font.render("Player 1 Wins!", True, FONT_COLOR)
    elif player2_score > player1_score:
        result_text = font.render("Player 2 Wins!", True, FONT_COLOR)
    else:
        result_text = font.render("It's a Tie!", True, FONT_COLOR)

    screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(5000)

# Menu principal
def main_menu():
    while True:
        screen.fill(SCREEN_COLOR)
        title = font.render("PONG GAME", True, FONT_COLOR)
        single_player = font.render("1. Single Player", True, FONT_COLOR)
        multi_player = font.render("2. Multiplayer", True, FONT_COLOR)
        quit_game = font.render("3. Quit", True, FONT_COLOR)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(single_player, (SCREEN_WIDTH // 2 - single_player.get_width() // 2, 200))
        screen.blit(multi_player, (SCREEN_WIDTH // 2 - multi_player.get_width() // 2, 300))
        screen.blit(quit_game, (SCREEN_WIDTH // 2 - quit_game.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pong_game(multiplayer=False)
                if event.key == pygame.K_2:
                    pong_game(multiplayer=True)
                if event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

# Executar o menu principal
main_menu()
