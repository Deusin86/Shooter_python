import random
import os
import pygame
import math
from Menu import Menu

from spritesheet_functions import SpriteSheet

# from Menu import Menu
# --- Global constants ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 238)
RED = (255, 0, 0)
GREEN = (0,255,0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

size = (SCREEN_WIDTH, 2080)
nave = pygame.image.load("racecar.png")
inimigo = pygame.image.load("inimigo.png")
boss= pygame.image.load("boss.png")

bala1 = pygame.image.load('tiro1.png')
laser=pygame.image.load('laser.png')
second=pygame.image.load('second.png')
missil=pygame.image.load('Torpedo3.png')

nave2 = pygame.image.load("racecar.png")
nave2_mini=pygame.transform.smoothscale(nave2,(15,15))
nave2_mini.set_colorkey(BLACK)

#Mouse estado
LEFT = 1
RIGHT = 3
font_name = pygame.font.match_font('arial')

#imagem_fundo = pygame.image.load("campo.jpg")

# bola = pygame.image.load("bola2.png")

# Controla tamnaho da imagem de fundo
#fundo = pygame.transform.scale(imagem_fundo, (size))

counter=int(0)
pygame.time.set_timer(pygame.USEREVENT, 500)
pygame.time.set_timer(pygame.USEREVENT + 7, 1000)

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []

explo_blue={}
explo_blue['lg']=[]
explo_blue['sm']=[]

powerup_images = {}



# --- Classes ---

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
        self.game_over = False
        self.ponto = 0
        self.imagem_fundo = pygame.image.load("space.jpg")
        self.fundo = pygame.transform.scale(self.imagem_fundo, (size))
        self.y=0

        self.cont=0
        self.cont1=1
        self.entra_boss=False

        #MENU
        self.menu = Menu(("start", "about", "exit"), font_color=WHITE, font_size=50,ttf_font="kenvector_future.ttf")
        self.show_about_frame = False  # True: display about frame of the menu
        self.show_menu = True

        # Create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.bala1_list = pygame.sprite.Group()
        self.laser_list= pygame.sprite.Group()
        self.arma2_list = pygame.sprite.Group()

        self.nave_list=pygame.sprite.Group()
        self.block_list = pygame.sprite.Group()
        self.boss_list=pygame.sprite.Group()

        self.poderes_list=pygame.sprite.Group()

        self.missil_list=pygame.sprite.Group()
        self.missil2_list=pygame.sprite.Group()
        self.laser_boss_list=pygame.sprite.Group()


        self.nave = Nave()
        self.all_sprites_list.add(self.nave)
        self.nave_list.add(self.nave)
        for i in range(5):
            self.inimigo = Inimigo()
            self.block_list.add(self.inimigo)
            self.all_sprites_list.add(self.inimigo)

        #BAlas inimigo
        self.laser=Bala2()

        #Balas do jogador
        self.bala1 = Bala()

        #Balas2 Do jogador
        self.second2=Segundo(0)

        self.poderes=Poderes(self.inimigo.rect.center)

        self.boss=Boss()

    @property
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                #  if self.game_over:
                #    self.__init__()
                self.bala1 = Bala()
                self.bala1.rect.x = self.nave.rect.x
                self.bala1.rect.y = self.nave.rect.y
                self.bala1_list.add(self.bala1)
                self.all_sprites_list.add(self.bala1)



            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                print("DONW")
                self.all_sprites_list.add(self.second2)
                self.arma2_list.add(self.second2)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
                print("UP")

                self.all_sprites_list.remove(self.second2)
                self.arma2_list.remove(self.second2)

            elif event.type==pygame.USEREVENT:
                self.shoot()
                self.shoot_boss()

            elif event.type==pygame.USEREVENT+7:
                self.shoot_boss2()

          #  elif event.type == pygame.KEYDOWN:
           #     if event.key == pygame.K_ESCAPE:
            #        return True

            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.show_menu and not self.show_about_frame:
                        if self.menu.state == 0:
                            self.show_menu = False
                            print("ola")
                            if len(self.block_list)==0:
                                self.restart()
                                self.all_sprites_list.add(self.nave)
                                self.nave_list.add(self.nave)
                        elif self.menu.state == 1:
                            self.show_about_frame = True
                            print("oi")
                        elif self.menu.state == 2:
                            # User clicked exit
                            print("exit")
                            return True

                elif event.key == pygame.K_ESCAPE:
                    if event.key == pygame.K_ESCAPE:
                        self.show_menu=True
                        self.show_about_frame=False
                        self.nave.reset()
                        self.boss.reset()
                        self.entra_boss=False
                        for self.inimigo in self.block_list:
                            pygame.sprite.Sprite.kill(self.inimigo)
                        for self.laser in self.laser_list:
                            pygame.sprite.Sprite.kill(self.laser)
                        for self.missil in self.missil_list:
                            pygame.sprite.Sprite.kill(self.missil)
                        for self.missil2 in self.missil2_list:
                            pygame.sprite.Sprite.kill(self.missil2)
                        for self.laser_boss in self.laser_boss_list:
                            pygame.sprite.Sprite.kill(self.laser_boss)
                        for self.boss in self.boss_list:
                            pygame.sprite.Sprite.kill(self.boss)
                        for self.bala1 in self.bala1_list:
                           pygame.sprite.Sprite.kill(self.bala1)
                        self.ponto=0
                        self.cont=0
                        self.y=0
                       # return True

        return False

    def shoot(self):
        #MUITO IMPORTANTE
      #  hugo=int(0)
      #  ran=int(0)
      #  hugo=random.randint(1,25)
      #  while hugo==ran:
       #     hugo=random.randint(1,25)


        #ran=hugo
        #if ran == 5:
        for self.inimigo in self.block_list:
            self.laser = Bala2()
            self.laser.rect.x = self.inimigo.rect.x
            self.laser.rect.y = self.inimigo.rect.y
            self.all_sprites_list.add(self.laser)
            self.laser_list.add(self.laser)

    def shoot_boss(self):

        if self.cont==5:
            for self.boss in self.boss_list:
                self.missil = Missil()
                self.missil.rect.x = self.boss.rect.x-10
                self.missil.rect.y = self.boss.rect.y
                self.missil_list.add(self.missil)
                self.all_sprites_list.add(self.missil)

                self.missil2 = Missil2()
                self.missil2.rect.x = self.boss.rect.x+60
                self.missil2.rect.y = self.boss.rect.y
                self.missil2_list.add(self.missil2)
                self.all_sprites_list.add(self.missil2)


    def shoot_boss2(self):
        if self.cont==5:
            for self.boss in self.boss_list:
                self.laser_boss = Laser_boss(self.nave.rect.x,0)
                self.laser_boss.rect.x, self.laser_boss.rect.y = self.boss.rect.center
                self.laser_boss_list.add(self.laser_boss)
                self.all_sprites_list.add(self.laser_boss)



    def mostra_vida(self,screen,x,y,vida,img):
        for i in range(vida):
            img_rect=img.get_rect()
            img_rect.x=x+20*i
            img_rect.y=y
            screen.blit(img,img_rect)

    def escudo_bar(self,screen, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(screen, GREEN, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 2)

    def desenhar_texto(self,screen, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)


    def restart(self):
        for i in range(5):
            self.inimigo = Inimigo()
            self.block_list.add(self.inimigo)
            self.all_sprites_list.add(self.inimigo)

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """

        #if not self.game_over:
            # Move all the sprites
        if not self.show_menu:

            self.all_sprites_list.update()
            #COLLIDER BALA AZUL COM INIMIGO
            for self.inimigo in self.block_list:
                self.block_hit_list=pygame.sprite.spritecollide(self.inimigo, self.bala1_list,True)
                for self.bala1 in self.block_hit_list:
                    self.inimigo.vida-=self.bala1.dano
                    exp=ExplosionPLY(self.inimigo.rect.center,"sm")
                    self.all_sprites_list.add(exp)

                 #   print(self.inimigo.vida)
                    if self.inimigo.vida==0:
                        self.ponto += 10
                        if random.random() > 0.3:
                            print("poderes")
                            self.poderes=Poderes(self.inimigo.rect.center)
                            self.all_sprites_list.add(self.poderes)
                            self.poderes_list.add(self.poderes)
                        self.block_list.remove(self.inimigo)
                        self.all_sprites_list.remove(self.inimigo)
                        exp=ExplosionPLY(self.inimigo.rect.center,"lg")
                        self.all_sprites_list.add(exp)
                        self.cont += self.cont1
                       # self.bala1_list.remove(self.bala1)



            #COLIIDER TIRO VERDE COM INIMIGO
            for self.second2 in self.arma2_list:
                self.arame_hit=pygame.sprite.spritecollide(self.second2, self.block_list,False)

                for self.inimigo in self.arame_hit:
                    self.inimigo.vida -= self.second2.dano
                    print(self.inimigo.vida)
                    if self.inimigo.vida==0:
                        self.ponto += 10
                        self.block_list.remove(self.inimigo)
                        self.arma2_list.remove(self.inimigo)
                        self.all_sprites_list.remove(self.inimigo)
                        self.cont+=self.cont1


            #COLLIDER ARMA COM LASER RED
            for self.laser in self.laser_list:
                self.arma2_hit=pygame.sprite.spritecollide(self.laser,self.arma2_list,True)

            #COLLIDER PODERES PLAYER
            for self.nave in self.nave_list:
                self.poderes_hit=pygame.sprite.spritecollide(self.nave,self.poderes_list,False)
                for self.poderes in self.poderes_hit:
                    if self.poderes.type == 'escudo':
                        if self.nave.escudo>=50:
                            self.nave.escudo=100
                            self.all_sprites_list.remove(self.poderes)
                            self.poderes_list.remove(self.poderes)
                            self.poderes_hit.remove(self.poderes)
                        elif self.nave.escudo<50:
                            self.nave.escudo=50
                            self.all_sprites_list.remove(self.poderes)
                            self.poderes_list.remove(self.poderes)
                            self.poderes_hit.remove(self.poderes)
                    elif self.poderes.type == 'vida':
                        if self.nave.vida==5:
                            self.all_sprites_list.remove(self.poderes)
                            self.poderes_list.remove(self.poderes)
                            self.poderes_hit.remove(self.poderes)
                        elif self.nave.vida==4:
                            self.nave.vida=5
                            self.all_sprites_list.remove(self.poderes)
                            self.poderes_list.remove(self.poderes)
                            self.poderes_hit.remove(self.poderes)
                        elif self.nave.vida==3:
                            self.nave.vida=4
                            self.all_sprites_list.remove(self.poderes)
                            self.poderes_list.remove(self.poderes)
                            self.poderes_hit.remove(self.poderes)
                        elif self.nave.vida==2:
                            self.nave.vida=3
                            self.all_sprites_list.remove(self.poderes)
                            self.poderes_list.remove(self.poderes)
                            self.poderes_hit.remove(self.poderes)
                        elif self.nave.vida==1:
                            self.nave.vida=2
                            self.all_sprites_list.remove(self.poderes)
                            self.poderes_list.remove(self.poderes)
                            self.poderes_hit.remove(self.poderes)


            for self.nave in self.nave_list:
                self.nave_hit_list=pygame.sprite.spritecollide(self.nave,self.laser_list,True)

                for self.laser in self.nave_hit_list:
                    self.nave.escudo-=self.laser.dano*25
                    #print(self.nave.escudo)
                    exp1 = ExplosionINI(self.nave.rect.center, "sm")
                    self.all_sprites_list.add(exp1)
                    if self.nave.escudo<=0:
                        self.nave.vida -= self.laser.dano
                        self.ponto-=5
                        self.all_sprites_list.add(exp1)
                  #  print(self.nave.vida)
                    if self.nave.vida ==0:
                        self.nave_list.remove(self.nave)
                        self.all_sprites_list.remove(self.nave)
                        exp1 = ExplosionINI(self.nave.rect.center, "lg")
                        self.all_sprites_list.add(exp1)


            if self.cont==5:
                self.entra_boss=True

            #CRIA O BOSS
          #  if self.ponto==50:
            if self.entra_boss:
                # self.boss.rect.x=self.nave.rect.x-35
                self.boss_list.add(self.boss)
                self.all_sprites_list.add(self.boss)

            # COLLIDERS do BOSS
            for self.boss in self.boss_list:
                self.boss22_hits=pygame.sprite.spritecollide(self.boss,self.bala1_list,True)
                for self.bala1 in self.boss22_hits:
                    self.boss.vida -= self.bala1.dano
              #      self.ponto+=self.bala1.dano
                    print(self.boss.vida)
                    #exp = ExplosionPLY(self.inimigo.rect.center, "sm")
                    #self.all_sprites_list.add(exp)
                    if self.boss.vida==0:
                        self.cont += self.cont1
                        self.ponto+=100
                        self.entra_boss=False
                        self.boss_list.remove(self.boss)
                        self.all_sprites_list.remove(self.boss)

            #COLLIDER MISSIL WITH PLAYER
            for self.nave in self.nave_list:
                self.missil_hit=pygame.sprite.spritecollide(self.nave,self.missil_list,True)
                for self.missil in self.missil_hit:
                    self.nave.escudo-=self.missil.dano*25
                    if self.nave.escudo<=0:
                        self.nave.vida-=self.missil.dano
                        if self.nave.vida<=0:
                            self.all_sprites_list.remove(self.nave)
                            self.nave_list.remove(self.nave)


            #CoLLIDER MISSIL2 WITH PLAYER
            for self.nave in self.nave_list:
                self.missil2_hit = pygame.sprite.spritecollide(self.nave, self.missil2_list, True)
                for self.missil2 in self.missil2_hit:
                    self.nave.escudo -= self.missil2.dano * 25
                    if self.nave.escudo <= 0:
                        self.nave.vida -= self.missil2.dano
                        if self.nave.vida <= 0:
                            self.all_sprites_list.remove(self.nave)
                            self.nave_list.remove(self.nave)


            #COLLIDER RED COM NAVE
            for self.nave in self.nave_list:
                self.laser_boss_hit=pygame.sprite.spritecollide(self.nave, self.laser_boss_list,True)
                for self.laser_boss in self.laser_boss_hit:
                    self.nave.escudo-=self.laser_boss.dano * 25
                    if self.nave.escudo<=0:
                        self.nave.vida-=self.laser_boss.dano
                        if self.nave.vida<=0:
                            self.all_sprites_list.remove(self.nave)
                            self.nave_list.remove(self.nave)


            #COLLIDER VERD COM BOSS
            for self.boss in self.boss_list:
                self.laser_verde_hit=pygame.sprite.spritecollide(self.boss,self.arma2_list,False)
                for self.second2 in self.laser_verde_hit:
                    self.boss.vida-=self.second2.dano
                    if self.boss.vida<=0:
                        self.ponto+=100
                        self.entra_boss=False
                        self.cont+=self.cont1
                        self.all_sprites_list.remove(self.boss)
                        self.boss_list.remove(self.boss)


            #COLLIDER MISSIl COM BALA AZUL
            for self.missil in self.missil_list:
                self.missil_boss_hit=pygame.sprite.spritecollide(self.missil,self.bala1_list,False)
                #print(self.missil.vida)
                for self.bala1 in self.missil_boss_hit:
                    print(self.missil.vida)
                   # print(self.bala1.dano)
                    self.missil.vida-=self.bala1.dano
                    self.bala1_list.remove(self.bala1)
                    self.all_sprites_list.remove(self.bala1)
                    if self.missil.vida<=0:
                        if random.random() > 0.2:
                            print("poderes")
                            self.poderes = Poderes(self.missil.rect.center)
                            self.all_sprites_list.add(self.poderes)
                            self.poderes_list.add(self.poderes)
                        self.missil_list.remove(self.missil)
                        self.all_sprites_list.remove(self.missil)

            # COLLIDER MISSI2 COM BALA AZUL
            for self.missil2 in self.missil2_list:
                self.missil2_boss_hit = pygame.sprite.spritecollide(self.missil2, self.bala1_list, False)

                for self.bala1 in self.missil2_boss_hit:
                  #      print(self.missil2.vida)
                        # print(self.bala1.dano)
                    self.missil2.vida -= self.bala1.dano
                    self.bala1_list.remove(self.bala1)
                    self.all_sprites_list.remove(self.bala1)
                    if self.missil2.vida <= 0:
                        if random.random() > 0.2:
                        #        print("poderes")
                            self.poderes = Poderes(self.missil2.rect.center)
                            self.all_sprites_list.add(self.poderes)
                            self.poderes_list.add(self.poderes)
                        self.missil2_list.remove(self.missil2)
                        self.all_sprites_list.remove(self.missil2)

            # COLLIDER MISSIl COM BALA VERDE
            for self.missil in self.missil_list:
                self.verde_boss_hit = pygame.sprite.spritecollide(self.missil, self.arma2_list, False)
                    # print(self.missil.vida)
                for self.second2 in self.verde_boss_hit:
                    print(self.missil.vida)
                        # print(self.bala1.dano)
                    self.missil.vida -= self.second2.dano
                    if self.missil.vida <= 0:
                        if random.random() > 0.2:
                #                print("poderes")
                            self.poderes = Poderes(self.missil.rect.center)
                            self.all_sprites_list.add(self.poderes)
                            self.poderes_list.add(self.poderes)
                        self.missil_list.remove(self.missil)
                        self.all_sprites_list.remove(self.missil)

            # COLLIDER MISSIl2 COM BALA VERDE
            for self.missil2 in self.missil2_list:
                self.verde2_boss_hit = pygame.sprite.spritecollide(self.missil2, self.arma2_list, False)
                    # print(self.missil.vida)
                for self.second2 in self.verde2_boss_hit:
                    print(self.missil.vida)
                        # print(self.bala1.dano)
                    self.missil2.vida -= self.second2.dano
                    if self.missil2.vida <= 0:
                        if random.random() > 0.2:
                            print("poderes")
                            self.poderes = Poderes(self.missil2.rect.center)
                            self.all_sprites_list.add(self.poderes)
                            self.poderes_list.add(self.poderes)
                        self.missil2_list.remove(self.missil2)
                        self.all_sprites_list.remove(self.missil2)



    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)
        # background
        #Cria uma Background e desenha no topo e apanha as coordenadas
        rel_y=self.y % self.fundo.get_rect().height
        #Desenha no ecran a imgem de top e com essa esta co o self.y começa a descer
        screen.blit(self.fundo, [0,rel_y-self.fundo.get_rect().height])
     #   if rel_y<=SCREEN_HEIGHT:
        #Desenha Background no centro do ecra como o rel_y te o tal sel.y esta desce
        screen.blit(self.fundo, [0, rel_y])
        self.y += 1

        self.desenhar_texto(screen, str('Vidas:'), 15, SCREEN_WIDTH-125, 0)
        self.mostra_vida(screen,SCREEN_WIDTH-100,5,self.nave.vida,nave2_mini)
        self.desenhar_texto(screen,str('Escudo:'),15,20,0)
        self.escudo_bar(screen,50,5,self.nave.escudo)

        self.desenhar_texto(screen,str(self.ponto),20,SCREEN_WIDTH / 2,0)

        if not self.game_over:
            self.all_sprites_list.draw(screen)

            time_wait = False
            if self.show_menu:
                if self.show_about_frame:
                    # Display the about frame
                    self.desenhar_texto(screen, str('Hugo'), 15, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                else:
                    # Display the menu
                    self.menu.display_frame(screen)


            if self.nave.vida<=0:
                self.desenhar_texto(screen,str('GAME OVER'),40,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                time_wait=True
                self.show_menu = True
                self.show_about_frame = False
                self.nave.reset()
                self.boss.reset()
                self.entra_boss = False
                for self.inimigo in self.block_list:
                    pygame.sprite.Sprite.kill(self.inimigo)
                for self.laser in self.laser_list:
                    pygame.sprite.Sprite.kill(self.laser)
                for self.missil in self.missil_list:
                    pygame.sprite.Sprite.kill(self.missil)
                for self.missil2 in self.missil2_list:
                    pygame.sprite.Sprite.kill(self.missil2)
                for self.laser_boss in self.laser_boss_list:
                    pygame.sprite.Sprite.kill(self.laser_boss)
                for self.boss in self.boss_list:
                    pygame.sprite.Sprite.kill(self.boss)
                for self.bala1 in self.bala1_list:
                    pygame.sprite.Sprite.kill(self.bala1)
                self.ponto = 0
                self.cont = 0
                self.y = 0

            pygame.display.flip()
            if time_wait:
                pygame.time.wait(3000)


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 30
        self.y = 30
        self.image = pygame.transform.smoothscale(nave, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT-50)
        self.pos = pygame.mouse.set_pos(self.rect.center)
        self.vida=5
        self.escudo=100

    def update(self):

        pos = pygame.mouse.get_pos()
        # pygame.event.set_grab(False)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.virifica = pygame.mouse.get_focused(True)
        if not self.virifica and self.rect.right >= SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.x
        elif not self.virifica and self.rect.bottom >= SCREEN_HEIGHT:
            # oi=pygame.mouse.get_pos()
            #  print(oi)
            self.rect.y = SCREEN_HEIGHT - self.y

    def reset(self):
        self.x = 30
        self.y = 30
        self.image = pygame.transform.smoothscale(nave, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
        self.pos = pygame.mouse.set_pos(self.rect.center)
        self.vida = 5
        self.escudo = 100




   # def mostra_vida(self, screen, x, y, vida, img):
    #    for i in range(vida):
     #       img_rect = img.get_rect()
     #       img_rect.x = x + 30 * 1
      #      img_rect.y = y
       #     screen.blit(img, img_rect)






class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.smoothscale(inimigo, (30, 30))
        self.rect = self.image.get_rect()
        # self.rect.center=(SCREEN_WIDTH/2, -20)
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = 1
        self.velx = random.randint(-3, 3)
        self.vely = -random.randint(3,5)
        self.vida=5
      #  self.teste2 = 50

    def update(self):
        self.rect.x += self.velx
        self.rect.y -= self.vely

       # self.teste+=self.teste2
        #  print(self.velx)



        if self.rect.right >= SCREEN_WIDTH and self.velx > 0:
            self.vely *= 1
            self.velx *= -1
        elif self.rect.left <= 0 and self.velx < 0:
            self.velx *= -1
            self.vely *= 1

        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.reset_pos()

    def reset_pos(self):
        self.image = pygame.transform.smoothscale(inimigo, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH)  # random.randrange(SCREEN_WIDTH)
        self.rect.y = 1  # random.randrange(-300, SCREEN_HEIGHT)
        self.velx = random.randint(-3, 3)
        self.vely = -3
      #  self.teste=500
    #    self.teste2 = -25

    def reset_all(self):

        self.image = pygame.transform.smoothscale(inimigo, (30, 30))
        self.rect = self.image.get_rect()
        # self.rect.center=(SCREEN_WIDTH/2, -20)
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = 1
        self.velx = random.randint(-3, 3)
        self.vely = -random.randint(3, 5)
        self.vida = 1



class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.smoothscale(boss, (100, 80))
        self.rect = self.image.get_rect()
        self.rect.x =SCREEN_WIDTH/2
        self.rect.y =SCREEN_HEIGHT-SCREEN_HEIGHT-70
        self.vida=30
        self.vely=1
        self.velx=1

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely


        if self.rect.y==100:
            self.vely=0

        if self.rect.right >= SCREEN_WIDTH and self.velx > 0:
            self.velx *= -1

        elif self.rect.left <= 0 and self.velx < 0:
            self.velx *= -1

        if self.vida==0:
            self.kill()

    def reset(self):
        self.image = pygame.transform.smoothscale(boss, (100, 80))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - SCREEN_HEIGHT - 70
        self.vida = 30
        self.vely = 1
        self.velx = 1



class Bala(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 15
        self.y = 15
        self.image = pygame.transform.smoothscale(bala1, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.vely = 5
        self.dano=1
        self.vida=1

    def update(self):
        self.rect.y -= self.vely

        if self.rect.top < 0:
            self.kill()



class Bala2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 15
        self.y = 15
        self.image = pygame.transform.smoothscale(laser, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.vely = -5
        self.dano=1

    def update(self):

        self.rect.y -= self.vely

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()


class Segundo(pygame.sprite.Sprite):
    def __init__(self,time):
        super().__init__()
        self.x = 15
        self.y = 100
        self.image = pygame.transform.smoothscale(second, (self.x, self.y))
        self.rect = self.image.get_rect()
       # self.vely = 5
        self.dano=1
        self.time=time
        self.time_counter=1

    def update(self):

        self.time += self.time_counter
        print(self.time)



        if self.time<20:

            pos = pygame.mouse.get_pos()
            self.rect.x = pos[0] + 6
            self.rect.y = pos[1] - 100

        elif self.time>=20:
            self.kill()
            self.time=0



class Missil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 15
        self.y = 20
        self.image = pygame.transform.smoothscale(missil, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.velx=-5
        self.vely=3
        self.dano =2
        self.vida=2


    def update(self):
        self.rect.y += self.vely
        self.rect.x+=self.velx

      #  print(self.velx)
       # print(self.vely)
        #(self.dx, self.dy) = ((self.X - self.rect.x) / math.sqrt((self.X - self.rect.x) ** 2 + (self.Y - self.rect.y) ** 2),
       #             (self.Y - self.rect.y) / math.sqrt((self.X - self.rect.x) ** 2 + (self.Y - self.rect.y) ** 2))

      #  (self.dx, self.dy) = ((self.X - self.x) / math.sqrt((self.X - self.x) ** 2 + (self.Y - self.y) ** 2),
       #              (self.Y - self.y) / math.sqrt((self.X - self.x) ** 2 + (self.Y - self.y) ** 2))

        #self.rect.x = self.X + self.dx * 2
        #self.rect.y = self.Y + self.dy * 2


        if self.rect.right >= SCREEN_WIDTH and self.velx > 0:
            self.vely *= 1
            self.velx *= -1
        elif self.rect.left <= 0 and self.velx < 0:
            self.velx *= -1
            self.vely *= 1
        if self.rect.bottom >= SCREEN_HEIGHT:
                self.kill()


class Missil2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 15
        self.y = 20
        self.image = pygame.transform.smoothscale(missil, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.velx=5
        self.vely=3
        self.dano = 2
        self.vida=2

#TESTAR

    #def update(self):
      #  self.desx=((self.X - self.rect.x) / math.sqrt((self.X - self.rect.x) ** 2 + (self.Y - self.rect.y) ** 2))
       # self.rect.x+=self.desx*self.velx

        #self.desy=((self.Y - self.rect.y) / math.sqrt((self.X - self.rect.x) ** 2 + (self.Y - self.rect.y) ** 2))
        #self.rect.y-=self.desy*self.vely


        #if self.rect.bottom >= SCREEN_HEIGHT:
         #   self.kill()

    def update(self):
        self.rect.y += self.vely
        self.rect.x+=self.velx


        if self.rect.right >= SCREEN_WIDTH and self.velx > 0:
            self.vely *= 1
            self.velx *= -1
        elif self.rect.left <= 0 and self.velx < 0:
            self.velx *= -1
            self.vely *= 1
        if self.rect.bottom >= SCREEN_HEIGHT:
                self.kill()


class Laser_boss(pygame.sprite.Sprite):
    def __init__(self,X,Y):
        super().__init__()
        self.x = 15
        self.y = 20
        self.image = pygame.transform.smoothscale(laser, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.velx=25
        self.vely=15
        self.dano = 2
        self.X=X
        self.Y=Y

#TESTAR

    def update(self):
        self.desx=((self.X - self.rect.x) / math.sqrt((self.X - self.rect.x) ** 2 + (self.Y - self.rect.y) ** 2))
        self.rect.x+=self.desx*self.velx

        self.desy=((self.Y - self.rect.y) / math.sqrt((self.X - self.rect.x) ** 2 + (self.Y - self.rect.y) ** 2))
        self.rect.y-=self.desy*self.vely


        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()



class ExplosionINI(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)


        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(os.path.join('img', filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (25, 25))
            explosion_anim['sm'].append(img_sm)



        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate =1

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class ExplosionPLY(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)


        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(os.path.join('img2', filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            explo_blue['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (25, 25))
            explo_blue['sm'].append(img_sm)



        self.size = size
        self.image = explo_blue[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate =1

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explo_blue[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explo_blue[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



class Poderes(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        powerup_images['escudo'] = pygame.image.load(os.path.join('img', 'escudo.png')).convert()
        powerup_images['vida'] = pygame.image.load(os.path.join('img', 'vida.png')).convert()
        self.type = random.choice(['escudo', 'vida'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()