# coding: UTF-8
# LUCAS GABRIEL SOARES DE ALMEIDA - PROG1 - UFCG - 2019.1

import pygame
from pygame.locals import *
from random import randint

from funcoes import melhor_caminho, colidiu, pinar

pygame.init()
pygame.font.init()
	
class posicao():
	def __init__(self, x, y, grav = 0):
		self.pos_x = x
		self.pos_y = y
		self.velocidade_x = 0
		self.velocidade_y = 0
		self.resistencia_x = 0.5
		self.gravidade = grav
		
	def getResistenciaX(self):
		return self.resistencia_x
	def getGravidade(self):
		return self.gravidade
		
	def setVelocidadeX(self, new):
		self.velocidade_x = new
	def addVelocidadeX(self, new):
		self.velocidade_x += new
	def getVelocidadeX(self):
		return self.velocidade_x
		
	def setVelocidadeY(self, new):
		self.velocidade_y = new
	def addVelocidadeY(self, new):
		self.velocidade_y += new
	def getVelocidadeY(self):
		return self.velocidade_y
		
		
	def setX(self, new):
		self.pos_x = new
	def setY(self, new):
		self.pos_y = new
	def getX(self):
		return self.pos_x
	def getY(self):
		return self.pos_y
	def spawnar(self, janela):
		janela.blit(self.image, (self.pos_x, self.pos_y))
		
class personagem(posicao):
	def __init__(self, size_x, size_y, path = False , x= 0, y= 0, grav = 0, tipo = 1, vel_inimigo = 1):
		posicao.__init__(self,x,y, grav)
		if path != False:
			temp = pygame.image.load(path).convert_alpha()
			self.image = pygame.transform.scale(temp, (size_x, size_y))
		self.lado = 1
		self.size = (size_x, size_y)
		self.tipo = tipo
		self.velocidade_inimigo = vel_inimigo
	def setVelocidadeInimigo(self, new):
		self.velocidade_inimigo = new
	def getVelocidadeInimigo(self):
		return self.velocidade_inimigo
	def getSize(self):
		return self.size
	def virarX(self):
		self.image = pygame.transform.flip(self.image, True, False)
	def getLado(self):
		return self.lado
	def mudarLado(self):
		self.lado = self.lado * -1
		
	def update_velocidade(self):
		if self.getGravidade() > 0 and self.tipo == 1:
			self.addVelocidadeY(self.getGravidade())
		else:
			self.setVelocidadeY(0)
		
		pressionadas = pygame.key.get_pressed()
		if pressionadas[K_UP] and self.tipo == 1:
			self.setVelocidadeY(-5)
		
		if self.tipo == 2:
			melhor = melhor_caminho(self, player, 10)
			self.setVelocidadeX(0)
			self.setVelocidadeY(0)
			if melhor == "cima":
				self.setVelocidadeY(-self.velocidade_inimigo)
			elif melhor == "esquerda":
				self.setVelocidadeX(-self.velocidade_inimigo)
			elif melhor == "baixo":
				self.setVelocidadeY(self.velocidade_inimigo)
			elif melhor == "direita":
				self.setVelocidadeX(self.velocidade_inimigo)
			
		
		if self.getVelocidadeX() > 0:
			self.setVelocidadeX(self.getVelocidadeX() - self.getResistenciaX())
		elif self.getVelocidadeX() < 0:
			self.setVelocidadeX(self.getVelocidadeX() + self.getResistenciaX())
			
		self.setX(self.getX()+self.getVelocidadeX())
		self.setY(self.getY()+self.getVelocidadeY())
		
class animacao(posicao):
	def __init__(self, tempo, tamanho, sprites, vezes = False,fps = 60):
		self.listImages = []
		self.size = tamanho
		for paths in sprites:
			temp = pygame.image.load(paths).convert_alpha()
			self.listImages.append(pygame.transform.scale(temp, self.size))
		self.status = 0
		self.tempoAtual = 0
		self.tempoTotal = tempo
		self.tempoCada = tempo/len(self.listImages)
		self.stop = False
		self.lado = 1
		self.vezes = vezes
	def getSize(self):
		return self.size
	def getStop(self):
		return self.stop
	def play(self):
		self.stop = False
		if self.tempoAtual >= self.tempoCada:
			self.tempoAtual = 0
			self.status += 1
		else:
			self.tempoAtual += 1
		if self.status >= len(self.listImages)-1:
			self.status = 0
			if self.vezes:
				self.stop = True
	def getImage(self):
		if self.stop != False:
			return self.listImages[0]
		return self.listImages[self.status]
	def stop(self):
		self.stop = True
	def spawnar(self, janela):
		janela.blit(self.getImage(), (self.pos_x, self.pos_y))
	def virarX(self):
		for im in range(len(self.listImages)):
			self.listImages[im] = pygame.transform.flip(self.listImages[im], True, False)
	def getLado(self):
		return self.lado
	def mudarLado(self):
		self.lado = self.lado * -1
#VARIAVEIS
tamanho_tela_x = 1280
tamanho_tela_y = 720
nome_janela = "LASANYA"
jogando = True
nivel = 1

# CONFIG TELA
tela = pygame.display.set_mode((tamanho_tela_x, tamanho_tela_y), pygame.FULLSCREEN)
pygame.display.set_caption(nome_janela)
relogio = pygame.time.Clock()
fps = 60

#CONSTANTES
path_player = "sprites/potatoSprite.png"
player = personagem(50, 55, path_player, 720, 500, 0.1)

path_hitbox = "sprites/hitbox.png"
hitbox = personagem(70, 70, path_hitbox, 100, 100)

espada = animacao(10, (100, 110), ["sprites/espada1.png","sprites/espada2.png","sprites/espada3.png","sprites/espada4.png","sprites/espada5.png","sprites/espada6.png"], True)
espadando = False

musica_tudo = pygame.mixer.music.load("sounds/musica.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0)

path_inimigo = "sprites/inimigo.png"
inimigos = []
velocidade_inimigo = 1
soma_velocidade_inimigo = 0.5

asas = animacao(50, (50,55), ["sprites/jetpack1.png", "sprites/jetpack2.png","sprites/jetpack3.png","sprites/jetpack4.png","sprites/jetpack5.png","sprites/jetpack6.png","sprites/jetpack7.png"])

# Cores
branco = (255,255,255)
preto = (0,0,0)
vermelho = (255,0,0)
cinza = (158,158,128)

# Cria fonte
fonteMain = pygame.font.SysFont('Comic Sans MS', 50)
fonteNivel = pygame.font.SysFont('Comic Sans MS', 20)
# Cria textos
textoIniciar = fonteMain.render(("Pressione espaco para iniciar"), 1, preto)
posicaoTextoIniciar = (300,300)

textoPausa = fonteMain.render(("Pressione espaco para voltar da pausa"), 1, preto)
posicaoTextoPausa= (150,300)

spawnZone = pygame.Surface((600, 400))
spawnZone.fill(vermelho)
spawnZone.set_alpha(50)

primeira = True

pausado = True
tela.fill(cinza)
tela.blit(textoIniciar,posicaoTextoIniciar)
pygame.display.update()
# LOOP
class main():
	while True:
		relogio.tick(fps)
		if not jogando:
			textoPerdeu = fonteMain.render(("Voce perdeu! \n Pontuacao: %i" %(nivel-1)), 1, preto)
			textoSair = fonteMain.render(("Pressione esc para sair"), 1, preto)
			textoTentar = fonteMain.render(("Pressione espaco para tentar novamente"), 1, branco)
			posicaoTextoPerdeu= (150,300)
			tela.fill(cinza)
			tela.blit(textoPerdeu, posicaoTextoPerdeu)
			tela.blit(textoSair, (150,400))
			tela.blit(textoTentar, (150,500))
			pressionadas = pygame.key.get_pressed()
			if pressionadas[K_ESCAPE]:
				pygame.quit()
				quit()
			if pressionadas[K_SPACE]:
				nivel = 0
				jogando = True
				inimigos = []
				velocidade_inimigo = 1
				soma_velocidade_inimigo = 0.05
				player.setX(720)
				player.setY(500)
			
		elif pausado:
			if not primeira:
				tela.blit(textoPausa,posicaoTextoPausa)
			pressionadas = pygame.key.get_pressed()
			if pressionadas[K_SPACE]:
				pausado = False
				primeira = False
		else:
			tela.fill(cinza)
			tela.blit(spawnZone, (0,0))
			textoNivel = fonteNivel.render(("Nivel: %i" %(nivel-1)), 1, preto)
			tela.blit(textoNivel, (1200, 0))
			if len(inimigos) == 0:
				nivel += 1
				velocidade_inimigo += soma_velocidade_inimigo
				for i in range(2+(nivel/2)):
					inimigo = personagem(50, 55, path_inimigo, randint(0, 600), randint(0, 400), tipo = 2, vel_inimigo = velocidade_inimigo)
					inimigos.append(inimigo)
			
			pressionadas = pygame.key.get_pressed()
			if pressionadas[K_RIGHT] and not pressionadas[K_LEFT]:
				if player.getLado() != 1:
					player.virarX()
					player.mudarLado()
				player.setVelocidadeX(5)
			if pressionadas[K_LEFT] and not pressionadas[K_RIGHT]:
				if player.getLado() != -1:
					player.virarX()
					player.mudarLado()
				player.setVelocidadeX(-5)
			if pressionadas[K_ESCAPE]:
					pausado = True
					
			for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == K_a and not espadando:
							espadando = True
							espada.play()
			if espadando:
				if espada.getStop():
					espadando = False
				else:
					espada.play()
				
				
			if player.getX() > tamanho_tela_x:
				player.setX(0)
			elif player.getX() < 0:
				player.setX(tamanho_tela_x)
			if player.getY() < 0:
				player.setY(0)
			if player.getY() > tamanho_tela_y - player.getSize()[1]:
				jogando = False
			player.update_velocidade()
			player.spawnar(tela)
			
			pinar(asas, player, -13, 5)
			asas.play()
			asas.spawnar(tela)
			
			pinar(hitbox, player, player.getSize()[0], 0)
			
			pinar(espada, player, player.getSize()[0]-5, -20)
			espada.spawnar(tela)
			
			for i in range(len(inimigos)-1, -1, -1):
				inimigos[i].update_velocidade()
				inimigos[i].spawnar(tela)
				try:
					if colidiu(hitbox, inimigos[i]) and espadando:
						inimigos.pop(i)
					if colidiu(inimigos[i], player):
						jogando = False
				except:
					print
		
		# EVENTOS
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quit()
		pygame.display.update()
