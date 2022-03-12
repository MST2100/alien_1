import pygame
import settings as s
import sys
from random import randint


def init_target():
    # load aliens der kommer ned fra oven
    aliens = []
    for tal in range(s.num_of_aliens):
        xpos = randint(s.delta, s.width - s.delta)
        ypos = 0
        speed = randint(1, 4)
        alien_rect = alien_img.get_rect(center=(xpos, ypos))
        alien = {"image": alien_img, "rect": alien_rect, "name": f"alien_{tal}", "counter": 0, "speed": speed}
        aliens.append(alien)
    return aliens

#starte spillet
pygame.init()

#lave counter
clock = pygame.time.Clock()

#forberede tekst
my_font = pygame.font.SysFont('arial', s.font_size)

#lave skærmen
screen = pygame.display.set_mode((s.width, s.height))

#loade billeder/elementer
bg = pygame.image.load("resources/bluebg.png")
ship = pygame.image.load("resources/ship.bmp")
ship_rect = ship.get_rect()
alien_img = pygame.image.load("resources/alien.bmp")
bg = pygame.transform.scale(bg,(s.width, s.height))
startknap = pygame.image.load("resources/start.jpg")

#loading targets into list:
aliens = init_target()


#variabler
alien_counter = 1
frame_counter = 0
frequency = 20
score = 0

#main loop
while True:
    frame_counter+= 1
    #følge musens position
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit(0)
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_s:
               s.start_game = not s.start_game

    #alien_counter der sørger for at sprede dem ud (count slower)
    if frame_counter % frequency == 0:
        alien_counter += 1
        if alien_counter == len(aliens):
            #hvis aliens når ud af counter, så start forfra:
            alien_counter = 1
            aliens = init_target()

    #sætte start-boolean til True
    if s.start_game == True:
        screen.blit(bg, (0, 0))
        #juster for skibene der kommer ned
        for alien in aliens[:alien_counter]:
            #hvis skib rammer alien ticker det point
            if ship_rect.colliderect(alien['rect']):
                score += 1
                alien['rect'].centerx=s.width+200
            else:
            #få bevægelse af aliens
                alien['rect'].centery+=alien['speed']
                #blit gør at den tegner billedet i spillet
                screen.blit(alien['image'], alien['rect'])
        #juster ship efter musen
        ship_rect.center = mouse_pos
    # paint stuff

        screen.blit(ship, ship_rect)

    else:
        #start-knappen
        screen.fill(s.white)
        screen.blit(startknap, (s.width/2, s.height/2))

    text = my_font.render(f"Score: {score}", True, s.white, s.black)
    screen.blit(text, text.get_rect())
    pygame.display.update()
    clock.tick(s.fr)
