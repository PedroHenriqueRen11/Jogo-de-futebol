import pygame
import sys
import random
import datetime
import pyttsx3
import speech_recognition as sr
from Recursos.funcoes import gerar_objeto_decorativo

pygame.init()
largura, altura = 1000, 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("FutGol 2D")

fonte = pygame.font.SysFont("Arial", 32)
preto = (0, 0, 0)
branco = (255, 255, 255)
amarelo = (255, 255, 0)

def capturar_nome_jogador():
    caixa = pygame.Rect(300, 300, 400, 50)
    fonte_input = pygame.font.Font(None, 40)
    texto = ""
    ativo = True

    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and texto.strip() != "":
                    return texto
                elif evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif len(texto) < 20:
                    texto += evento.unicode

        tela.fill((255, 255, 255))
        instrucao = fonte_input.render("Digite seu nome e pressione ENTER:", True, (0, 0, 0))
        tela.blit(instrucao, (200, 250))

        pygame.draw.rect(tela, (0, 0, 0), caixa, 2)
        txt_render = fonte_input.render(texto, True, (0, 0, 0))
        tela.blit(txt_render, (caixa.x + 10, caixa.y + 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)


fundo = pygame.image.load("Recursos/imagens/fundo.png")
jogador_img = pygame.image.load("Recursos/imagens/jogador.png")
bola_img = pygame.image.load("Recursos/imagens/bola.png")

voz = pyttsx3.init()
voz.say("Bem-vindo ao FutGol!")
voz.runAndWait()

reconhecedor = sr.Recognizer()

def reconhecer_comando():
    with sr.Microphone() as source:
        print("Diga: começar")
        audio = reconhecedor.listen(source)
        try:
            comando = reconhecedor.recognize_google(audio, language="pt-BR")
            return comando.lower()
        except:
            return ""

jogador = pygame.Rect(450, 550, 98, 142)
velocidade = 11

bola = pygame.Rect(random.randint(0, 936), 0, 64, 64)
bola_vel = 12

decorativo = gerar_objeto_decorativo()

raio = 30
sol_crescendo = True

pontos = 0
vidas = 3
pause = False

def tela_inicial(nome):
    while True:
        tela.fill(branco)
        texto1 = fonte.render(f"Bem-vindo, {nome}!", True, preto)
        texto2 = fonte.render("Acerte as bolas que caem com o jogador!", True, preto)
        texto3 = fonte.render("Pressione Enter para começar", True, preto)
        tela.blit(texto1, (300, 200))
        tela.blit(texto2, (250, 250))
        tela.blit(texto3, (270, 300))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return

nome = capturar_nome_jogador()
tela_inicial(nome)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                pause = not pause

    if pause:
        texto_pausa = fonte.render("PAUSE", True, preto)
        tela.blit(texto_pausa, (470, 300))
        pygame.display.flip()
        continue

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador.x > 0:
        jogador.x -= velocidade
    if teclas[pygame.K_RIGHT] and jogador.x < largura - jogador.width:
        jogador.x += velocidade

    bola.y += bola_vel
    if jogador.colliderect(bola):
        pontos += 1
        bola.x = random.randint(0, 936)
        bola.y = 0
    elif bola.y > altura:
        vidas -= 1
        bola.x = random.randint(0, 936)
        bola.y = 0

    if vidas <= 0:
        break

    decorativo["x"] += decorativo["vx"]
    decorativo["y"] += decorativo["vy"]
    if not (0 < decorativo["x"] < largura and 0 < decorativo["y"] < altura):
        decorativo = gerar_objeto_decorativo()

    if sol_crescendo:
        raio += 0.2
        if raio >= 40:
            sol_crescendo = False
    else:
        raio -= 0.2
        if raio <= 30:
            sol_crescendo = True

    tela.blit(fundo, (0, 0))
    tela.blit(jogador_img, jogador.topleft)
    tela.blit(bola_img, bola.topleft)
    pygame.draw.circle(tela, amarelo, (80, 80), int(raio))
    pygame.draw.circle(tela, (100, 200, 255), (int(decorativo["x"]), int(decorativo["y"])), 10)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, branco)
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, branco)
    pause_hint = fonte.render("Press Space to Pause Game", True, branco)
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_vidas, (10, 50))
    tela.blit(pause_hint, (700, 10))
    pygame.display.flip()
    pygame.time.delay(30)

data = datetime.datetime.now().strftime("%d/%m/%Y")
hora = datetime.datetime.now().strftime("%H:%M:%S")
with open("log.dat", "a") as f:
    f.write(f"{pontos} pontos | {data} | {hora}\n")

with open("log.dat", "r") as f:
    logs = f.readlines()[-5:]

while True:
    tela.fill(preto)
    texto_gameover = fonte.render("Fim de Jogo!", True, branco)
    tela.blit(texto_gameover, (420, 100))
    for i, linha in enumerate(logs):
        linha_txt = fonte.render(linha.strip(), True, branco)
        tela.blit(linha_txt, (300, 200 + i * 30))
    pygame.display.flip()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
