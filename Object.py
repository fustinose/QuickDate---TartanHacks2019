import pygame
from Settings import *
from Algorithm import faceDetection, findSimilarFaces
#The general template is by Lukas Pereza, from Pygame Manual
#https://qwewy.gitbooks.io/pygame-module-manual/chapter1/framework.html

# The following function is copied from 15-112 course website
import os
def listFiles(path):
    if (os.path.isdir(path) == False):
        # base case:  not a folder, but a file, so return singleton list with its path
        return [path]
    else:
        # recursive case: it's a folder, return list of all paths
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, image):
        super(Button, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x - self.width/2, self.y - self.width/2
        self.clicked = False

class Textbox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super(Textbox, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x - self.width/2, self.y - self.height/2
        self.text = ""
        self.selected = False



