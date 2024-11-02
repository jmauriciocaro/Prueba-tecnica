import pygame, random

from pygame.sprite import Group
#  1. Definimos colores y tamaño de la pantalla
WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

#2. iniciamos pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Meteroids")
clock = pygame.time.Clock()

#------------------FUNCIONES------------------
def pantalla_instrucciones():
    screen.fill(BLACK)
    dibujar_texto(screen, "Instrucciones", 65, WIDTH // 2, HEIGHT // 4)
    dibujar_texto(screen, "Mueve al jugador con las flechas izquierda y derecha", 27, WIDTH // 2, HEIGHT // 2 - 30)
    dibujar_texto(screen, "Dispara con la barra espaciadora para destruir meteoros", 27, WIDTH // 2, HEIGHT // 2)
    dibujar_texto(screen, "Presiona 'j' dos veces para jugar", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()

    # Espera a que el jugador presione 'j' para regresar al menú
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j:
                    waiting = False

def pantalla_game_over():
    screen.fill(BLACK)
    dibujar_texto(screen, "Menú", 65, WIDTH // 2, HEIGHT // 4)
    dibujar_texto(screen, "Presiona 'i' para instrucciones o 'j' para jugar", 27, WIDTH // 2, HEIGHT // 2)
    dibujar_texto(screen, "Presiona 'q' para salir", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_i:
                    pantalla_instrucciones()  # Muestra las instrucciones
                elif event.key == pygame.K_j:
                    waiting = False  # Empieza el juego
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def pantalla_nivel(nivel):
    screen.fill(BLACK)
    dibujar_texto(screen, f"NIVEL {nivel}", 65, WIDTH // 2, HEIGHT // 4)
    dibujar_texto(screen, "Presiona 'S' para continuar", 27, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    waiting = False 

    

def dibujar_texto(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def dibujar_vida(surface, x , y, vida):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    barra = (vida/100)* BAR_LENGHT
    borde = pygame.Rect(x,y,BAR_LENGHT,BAR_HEIGHT)
    barra = pygame.Rect(x,y,barra,BAR_HEIGHT)
    pygame.draw.rect(surface,GREEN,barra)
    pygame.draw.rect(surface,WHITE,borde,3) 




#------------------CLASES------------------

class Jugador(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK) #eliminamos el fondo de la imagen
        self.rect = self.image.get_rect() 
        #centgramos la posición en el centro de la imagen
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT-10
        self.speed_x = 0
        self.vida = 100
    
    def update(self) :
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def disparo(self):
        bala = Bala(self.rect.centerx,self.rect.top)
        all_sprites.add(bala)
        balas.add(bala)


class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #cargando imagen de los meteoros y centrando sus coordenadas
        self.image = random.choice(meteoro_imagenes)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #Aparición de los meteoros aleatoria, velocidades aleatorias
        self.rect.x = random.randrange(WIDTH- self.rect.width)
        self.rect.y = random.randrange(-200,-40)
        self.speedY = random.randrange(1,8)
        self.speedX = random.randrange (-5,5)
    
    def update(self):
        # velocidad de los meteoros y sus direcciones
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        # Reaparición de los meteoritos
        if self.rect.top > HEIGHT + 10 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedY = random.randrange(1, 10)
            self.speedX = random.randrange(-5, 5)

        # Creación del nivel 2                      
        if score > 20:
                    
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.speedX *= -1

        # Creación del nivel 3                

        if score > 40:
            
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.speedX *= -1
            
            # Colisiones entre meteoros
            for otro_meteoro in meteoro_list:
                if otro_meteoro != self and self.rect.colliderect(otro_meteoro.rect):
                    self.speedX *= -1
                    otro_meteoro.speedX *= -1

        
            



class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #velocidad de las balas y posición de salida
        self.rect.y = y
        self.rect.centerx = x
        self.speedY = -10
    
    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom < 0:
            self.kill()


#------------------FIN DE CLASES------------------


#3.Imagen de fondo
background = pygame.image.load("assets/background.png").convert()



meteoro_imagenes = []
meteoro_lista = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]  
for imagen in meteoro_lista:
    meteoro_imagenes.append(pygame.image.load(imagen).convert())     




#------FIN DEL JUEGO--------
game_over = True
running = True
nivel_flag = False
nivel = 1

#------FIN DEL JUEGO--------
game_over = True
running = True
nivel = 1

while running:
    if game_over:
        pantalla_game_over()
        
        # Reiniciar variables del juego al comenzar de nuevo
        game_over = False
        nivel_flag = False  # Reiniciar la bandera de nivel al empezar de nuevo
        nivel = 1  # Reiniciar al nivel 1
        all_sprites = pygame.sprite.Group()
        meteoro_list = pygame.sprite.Group()
        balas = pygame.sprite.Group()

        jugador = Jugador()
        all_sprites.add(jugador)

        for i in range(6):
            meteoro = Meteoro()
            all_sprites.add(meteoro)
            meteoro_list.add(meteoro)
        score = 0

    # Cambiar al nivel 2 cuando el puntaje es mayor a 20
    if score > 20 and nivel == 1:
        nivel += 1
        pantalla_nivel(nivel)
        nivel_flag = False  # Restablecer nivel_flag para permitir futuras pantallas de nivel

    # Cambiar al nivel 3 cuando el puntaje es mayor a 40
    if score > 40 and nivel == 2:
        nivel += 1
        pantalla_nivel(nivel)
        nivel_flag = False

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.disparo()

    # Cargar sprites
    all_sprites.update()
    
    # Colisiones meteoro vs laser
    golpes = pygame.sprite.groupcollide(meteoro_list, balas, True, True)
    for golpe in golpes:
        score += 1
        meteoro = Meteoro()
        all_sprites.add(meteoro)
        meteoro_list.add(meteoro) 

    # Verificar colisiones Jugador vs meteoro    
    golpes = pygame.sprite.spritecollide(jugador, meteoro_list, True)
    if golpes:
        jugador.vida -= 20
        meteoro = Meteoro()
        all_sprites.add(meteoro)
        meteoro_list.add(meteoro) 
        if jugador.vida == 0:
            game_over = True  # Al perder, vuelve a la pantalla de Game Over
    
    # Cargar fondo
    screen.blit(background, [0,0])
    all_sprites.draw(screen)

    # Marcador
    dibujar_texto(screen, str(score), 25, WIDTH // 2, 20)
    # Vida
    dibujar_vida(screen, 5, 5, jugador.vida)
    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
