import pygame, sys
from pygame.locals import *
 
pygame.init()
 
pygame.display.set_caption('font example')
size = [640, 480]
screen = pygame.display.set_mode(size)
 
clock = pygame.time.Clock()
 
basicfont = pygame.font.Font('/home/yash/gsoc/test-fonts/Roboto-Black.ttf', 72)
text = basicfont.render('Hello World!', True, (255, 0, 0), (255, 255, 255))
textrect = text.get_rect()
textrect.centerx = screen.get_rect().centerx
textrect.centery = screen.get_rect().centery
 
screen.fill((255, 255, 255))
screen.blit(text, textrect)
 
pygame.display.update()
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    clock.tick(20)