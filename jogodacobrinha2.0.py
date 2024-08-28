import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo da Cobrinha")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)

# Parâmetros da cobra
tamanhoQuadrado = 10
velocidadeJogo = 15

# Mapas e Obstáculos
obstaculos_mapa1 = []  # Map 1 can remain empty or contain other types of obstacles
obstaculos_mapa2 = [
    pygame.Rect(100, 100, 200, 50),  # Obstáculo maior
    pygame.Rect(600, 400, 150, 40)   # Obstáculo maior
]

def gerarComida(cobra_pixels, obstaculos):
    while True:
        comidaX = round(random.randrange(0, largura - tamanhoQuadrado) / float(tamanhoQuadrado)) * float(tamanhoQuadrado)
        comidaY = round(random.randrange(0, altura - tamanhoQuadrado) / float(tamanhoQuadrado)) * float(tamanhoQuadrado)
        comida_rect = pygame.Rect(comidaX, comidaY, tamanhoQuadrado, tamanhoQuadrado)
        if comida_rect.collidelist(obstaculos) == -1 and comida_rect.collidelist([pygame.Rect(px[0], px[1], tamanhoQuadrado, tamanhoQuadrado) for px in cobra_pixels]) == -1:
            return comidaX, comidaY

def desenharComida(tamanho, comidaX, comidaY):
    pygame.draw.rect(tela, verde, [comidaX, comidaY, tamanho, tamanho])

def desenharCobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenharPontuacao(pontuacao):
    fonte = pygame.font.SysFont("Comic Sans", 20)
    texto = fonte.render(f"Pontos: {pontuacao}", True, branca)
    tela.blit(texto, [10, 10])

def desenharTelaInicio():
    tela.fill(preta)
    fonte = pygame.font.SysFont("Comic Sans", 30)
    texto_titulo = fonte.render("Jogo da Cobrinha", True, verde)
    texto_instrucao = fonte.render("Pressione qualquer tecla para começar", True, verde)
    tela.blit(texto_titulo, [largura / 2 - texto_titulo.get_width() / 2, altura / 2 - texto_titulo.get_height() / 2 - 30])
    tela.blit(texto_instrucao, [largura / 2 - texto_instrucao.get_width() / 2, altura / 2 + 10])
    pygame.display.update()

def desenharTelaEscolhaMapa():
    tela.fill(preta)
    fonte = pygame.font.SysFont("Comic Sans", 30)
    texto_titulo = fonte.render("Escolha o Mapa", True, verde)
    texto_mapa1 = fonte.render("1: Mapa Padrão", True, verde)
    texto_mapa2 = fonte.render("2: Mapa com Desafios", True, verde)
    tela.blit(texto_titulo, [largura / 2 - texto_titulo.get_width() / 2, altura / 2 - texto_titulo.get_height() / 2 - 30])
    tela.blit(texto_mapa1, [largura / 2 - texto_mapa1.get_width() / 2, altura / 2])
    tela.blit(texto_mapa2, [largura / 2 - texto_mapa2.get_width() / 2, altura / 2 + 40])
    pygame.display.update()

def desenharTelaGameOver(pontuacao):
    tela.fill(preta)
    fonte = pygame.font.SysFont("Comic Sans", 30)
    texto_game_over = fonte.render("Game Over!", True, verde)
    texto_pontuacao = fonte.render(f"Sua pontuação: {pontuacao}", True, verde)
    tela.blit(texto_game_over, [largura / 2 - texto_game_over.get_width() / 2, altura / 2 - texto_game_over.get_height() / 2 - 30])
    tela.blit(texto_pontuacao, [largura / 2 - texto_pontuacao.get_width() / 2, altura / 2 + 10])
    pygame.display.update()
    pygame.time.wait(2000)

def selecionarVelocidade(tecla, velocidadeX, velocidadeY):
    if tecla == pygame.K_DOWN or tecla == pygame.K_s:
        if velocidadeY == 0:
            velocidadeX = 0
            velocidadeY = tamanhoQuadrado
    elif tecla == pygame.K_UP or tecla == pygame.K_w:
        if velocidadeY == 0:
            velocidadeX = 0
            velocidadeY = -tamanhoQuadrado
    elif tecla == pygame.K_RIGHT or tecla == pygame.K_d:
        if velocidadeX == 0:
            velocidadeX = tamanhoQuadrado
            velocidadeY = 0
    elif tecla == pygame.K_LEFT or tecla == pygame.K_a:
        if velocidadeX == 0:
            velocidadeX = -tamanhoQuadrado
            velocidadeY = 0
    return velocidadeX, velocidadeY

def desenharObstaculos(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, vermelho, obstaculo)

def colisaoComObstaculo(cobra_pixels, obstaculos):
    cobra_rects = [pygame.Rect(px[0], px[1], tamanhoQuadrado, tamanhoQuadrado) for px in cobra_pixels]
    for obstaculo in obstaculos:
        for cobra_rect in cobra_rects:
            if cobra_rect.colliderect(obstaculo):
                return True
    return False

def rodarJogo(obstaculos):
    fimJogo = False

    x = largura / 2
    y = altura / 2

    velocidadeX = 0
    velocidadeY = 0

    tamanhoCobra = 1
    pixels = []

    comidaX, comidaY = gerarComida(pixels, obstaculos)

    while not fimJogo:
        tela.fill(preta)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            elif evento.type == pygame.KEYDOWN:
                velocidadeX, velocidadeY = selecionarVelocidade(evento.key, velocidadeX, velocidadeY)

        # Atualizar a posição da cobra
        x += velocidadeX
        y += velocidadeY

        if x < 0 or x >= largura or y < 0 or y >= altura:
            fimJogo = True

        # Desenhar obstáculos
        desenharObstaculos(obstaculos)

        # Desenhar comida
        desenharComida(tamanhoQuadrado, comidaX, comidaY)

        # Atualizar corpo da cobra
        pixels.append([x, y])
        if len(pixels) > tamanhoCobra:
            del pixels[0]

        # Verificar colisão com o próprio corpo
        if [x, y] in pixels[:-1]:
            fimJogo = True

        # Verificar colisão com obstáculos
        if colisaoComObstaculo(pixels, obstaculos):
            fimJogo = True

        desenharCobra(tamanhoQuadrado, pixels)
        desenharPontuacao(tamanhoCobra - 1)

        # Criar nova comida se a cobra comer
        if x == comidaX and y == comidaY:
            tamanhoCobra += 1
            comidaX, comidaY = gerarComida(pixels, obstaculos)

        pygame.display.update()
        relogio.tick(velocidadeJogo)

    desenharTelaGameOver(tamanhoCobra - 1)

def main():
    # Tela de início
    desenharTelaInicio()
    iniciarJogo = False

    while not iniciarJogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                iniciarJogo = True

    # Tela de escolha de mapa
    desenharTelaEscolhaMapa()
    mapaSelecionado = None

    while mapaSelecionado is None: 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    mapaSelecionado = obstaculos_mapa1
                elif evento.key == pygame.K_2:
                    mapaSelecionado = obstaculos_mapa2

    rodarJogo(mapaSelecionado)
    pygame.quit()

if __name__ == "__main__":
    main()
