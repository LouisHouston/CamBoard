import pygame
import sys

# need this
pygame.init()


# Load sounds
sound1 = pygame.mixer.Sound("./sounds/crack.mp3")
sound2 = pygame.mixer.Sound("sounds/boom.mp3")
sound3 = pygame.mixer.Sound("sounds/wow.mp3")

# Testing funciton name 
def play_sound(soundNum):
    if soundNum == 1:
        sound1.play()
    if soundNum ==2:
        sound2.play()
    if soundNum == 3:
        sound3.play()
    return 0