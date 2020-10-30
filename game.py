import pygame
import sys
import random

from detect_colision import detect_colision_function

pygame.init()# iniciando o pygame

largura = 800#variavél para o pixel da largura da tela
altura = 600 #vairavél para o pixel da altura da tela

enemy_speed = 10

Vermelho = (255,0,0)#Criando a cor vermelha
Azul = (0,0,255)#Criando a cor azul
background_color = (70,80,70)#Criando a de fundo
Font_color = (0,0,0)#criando a cor da fonte

player_pos = [400,520]#Define a posição, 400 = longitude na tela, 300  = latitude na tela
player_size = 50 #Define como vai ser o tamanho do nosso objeto

enemy_size = 20 #Tamanho do nosso inimigo
enemy_pos = [random.randint(0,largura-enemy_size),20]#Posição do inimigo que aparecera em uma parte aleatória superior da tela
enemy_list = [enemy_pos]

tela = pygame.display.set_mode((largura, altura))# cria uma tela com 800 x 600 pixels

#criaremos um loop para o jogo ir rodando até ele não acabar
# segundo o video podemos pegar esse loop de uma biblioteca
game_over = False

score = 0

fps = pygame.time.Clock()

Font = pygame.font.SysFont("monospace",35)

def set_level(score,enemy_speed):
    if score < 20:
        enemy_speed = 15
    elif score < 40:
        enemy_speed = 20
    elif score < 60:
        enemy_speed = 30
    else:
        enemy_speed = 35
    return enemy_speed

def drop_enemies(enemy_list):
    delay = random.random()#os circulos só vão cair em um tempo certo por conta da var delay
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, largura - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.circle(tela, Azul, (enemy_pos[0], enemy_pos[1]),enemy_size)  # Desenhando o circulo que sera nosso inimigo

def update_enemy_positions(enemy_list,score):
    # Agora vamos fazer com o que o inimigo fique caindo na tela, no caso os circulos azuis
    for idx, enemy_pos in enumerate(enemy_list):

        if enemy_pos[1] >= 0 and enemy_pos[1] < largura:
            enemy_pos[1] += enemy_speed

        else:
            enemy_list.pop(idx)
            score += 1
    return score

def colision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_colision_function(enemy_pos,player_pos):
            return True
    return False


while game_over == False:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        #Agora vamos criar um evento para conseguir movimentar nosso personagem na tela
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]# para nosso player ir para os lados
            if event.key == pygame.K_LEFT:
                x -= player_size# mudando as posições da cordenada de x
            elif event.key == pygame.K_RIGHT:
                x += player_size# mudando as posições da cordenada de x

            y = player_pos[1]  # para nosso player ir para cima e para baixo
            if event.key == pygame.K_UP:
                y -= player_size  # mudando as posições da cordenada de y
            elif event.key == pygame.K_DOWN:
                y += player_size  # mudando as posições da cordenada de y

            player_pos = [x,y]
            # Com o código acima conseguimos fazer com que o retangulo ande
            # porém ele vai andar e continuar as marcações de onde ele estava antes, algo que não queremos
    if player_pos[1] >= altura or player_pos[1] < 0:
        game_over = False
        break
    if player_pos[0] < 0  or player_pos[0] >= largura:
        game_over = False
        break

    tela.fill(background_color) #Com isso criamos a cor de fundo e resolvemos o problema do retangulo


    if detect_colision_function(player_pos,enemy_pos):##chamando a função
        game_over = True
        break


    #Abaixo vamos criar nosso retangulo e definir a sua cor
    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list,score)
    enemy_speed = set_level(score,enemy_speed)

    text = "Pontuação:" + str(score)
    label = Font.render(text, 1, Font_color)
    tela.blit(label, (largura-250, altura-40))

    if colision_check(enemy_list, player_pos):
        game_over = True


    draw_enemies(enemy_list)
    pygame.draw.rect(tela,Vermelho,(player_pos[0],player_pos[1],player_size,player_size))#vamos criar um retangulo vermelho na tela



    fps.tick(20)


    pygame.display.update()#comando para o nosso retangulo vermelho aparecer na tela