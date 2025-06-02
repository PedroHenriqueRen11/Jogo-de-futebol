import pygame
import sys
import random
import datetime
import pyttsx3
import speech_recognition as sr
from Recursos.funcoes import gerar_objeto_decorativo

# Inicializações
pygame.init()
largura, altura = 1000, 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("FutGol 2D")

# Fontes e cores
fonte = pygame.font.SysFont("Arial", 32)
preto = (0, 0, 0)
branco = (255, 255, 255)
amarelo = (255, 255, 0)

# Sons
pygame.mixer.init()
chute_som = pygame.mixer.Sound("Recursos/sons/chute.wav")

# Imagens
fundo = pygame.image.load("Recursos/imagens/fundo.png")
jogador_img = pygame.image.load("Recursos/imagens/jogador.png")
bola_img = pygame.image.load("Recursos/imagens/bola.png")

# TTS com pyttsx3
voz = pyttsx3.init()
voz.say("Bem-vindo ao FutGol!")
voz.runAndWait()

# Reconhecimento de voz
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

# Jogador
jogador = pygame.Rect(450, 600, 64, 64)
velocidade = 5

# Bola
bola = pygame.Rect(random.randint(0, 936), 0, 64, 64)
bola_vel = 4

# Objeto decorativo
decorativo = gerar_objeto_decorativo()

# Sol
raio = 30
sol_crescendo = True

# Pontuação e vidas
pontos = 0
vidas = 3
pause = False

# Tela de boas-vindas
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

nome = input("Digite seu nome: ")
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

    # Movimento
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador.x > 0:
        jogador.x -= velocidade
    if teclas[pygame.K_RIGHT] and jogador.x < largura - jogador.width:
        jogador.x += velocidade

    # Atualizar bola
    bola.y += bola_vel
    if jogador.colliderect(bola):
        pontos += 1
        chute_som.play()
        bola.x = random.randint(0, 936)
        bola.y = 0
    elif bola.y > altura:
        vidas -= 1
        bola.x = random.randint(0, 936)
        bola.y = 0

    if vidas <= 0:
        break

    # Atualizar objeto decorativo
    decorativo["x"] += decorativo["vx"]
    decorativo["y"] += decorativo["vy"]
    if not (0 < decorativo["x"] < largura and 0 < decorativo["y"] < altura):
        decorativo = gerar_objeto_decorativo()

    # Atualizar sol pulsante
    if sol_crescendo:
        raio += 0.2
        if raio >= 40:
            sol_crescendo = False
    else:
        raio -= 0.2
        if raio <= 30:
            sol_crescendo = True

    # Desenhar tudo
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

# Fim de jogo e log
data = datetime.datetime.now().strftime("%d/%m/%Y")
hora = datetime.datetime.now().strftime("%H:%M:%S")
with open("log.dat", "a") as f:
    f.write(f"{pontos} pontos | {data} | {hora}\n")

# Tela de fim com últimos 5 registros
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
