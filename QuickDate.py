import pygame
from Settings import *
from Object import Button, Textbox
from Algorithm import faceDetection, findSimilarFaces, match, getInfo
import urllib
import io
import numpy as np
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


class PygameGame(object):

    def init(self):
        self.bg = pygame.transform.scale(pygame.image.load('images/bg.png').convert_alpha(), 
                    (800, 500))
        self.match = Button(WIDTH/2 - 10, HEIGHT/2, 80, pygame.transform.scale(pygame.image.load('images/match.png').convert_alpha(), BUTTON_SIZE))
        self.gameObjects = pygame.sprite.Group()
        self.gameObjects.add(self.match)
        self.result = None
        self.resultImage = None
        self.text = "https://"
        self.ideal = None
        self.confidence = None
        self.age = None
        self.gender = None
        self.database = np.load('database.npy').item()
        pygame.font.init()

    def mousePressed(self, x, y):
        if self.match.rect.collidepoint(x, y):
            self.match.clicked = True
        #elif self.box.rect.collidepoint(x, y):
         #   self.box.clicked = True

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass


    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_BACKSPACE and len(self.text) > 8:
            self.text = self.text[:-1]
        elif keyCode == pygame.K_RETURN:
            try:
                self.resultImage = None
                url = self.text
                imageStr = urllib.request.urlopen(str(url)).read()
                imageFile = io.BytesIO(imageStr)
                image = pygame.image.load(imageFile)
                imageRect = image.get_rect()
                w, h = imageRect.width, imageRect.height
                if w >= h:
                    ratio = h/w
                    scale = (200, int(200*ratio))
                else:
                    ratio = w/h
                    scale = (int(200*ratio), 200)
                self.ideal = pygame.transform.scale(image, scale)
            except:
                self.text = 'https://'
                self.ideal = None
                print('cannot read image')
        elif keyCode <= 127:
            self.text += chr(keyCode)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        # Match button process
        if self.match.clicked:
            if self.ideal != None:
                tmp = match(self.text)
                self.result, self.confidence = tmp['persistedFaceId'], tmp['confidence']
                self.confidence = round((((self.confidence + 1)/2+1)/2) * 100)
                self.match.clicked = False
                self.text = 'https://'
        if self.result != None:
            if self.result in self.database:
                try:
                    url = self.database[self.result]
                    print('url is:' + url)
                    imageStr = urllib.request.urlopen(str(url)).read()
                    print('read')
                    imageFile = io.BytesIO(imageStr)
                    print('load')
                    image = pygame.image.load(imageFile)
                    print('load again')
                    imageRect = image.get_rect()
                    w, h = imageRect.width, imageRect.height
                    if w >= h:
                        ratio = h/w
                        scale = (180, int(180*ratio))
                    else:
                        ratio = w/h
                        scale = (int(180*ratio), 180)
                    self.resultImage = pygame.transform.scale(image, scale)
                    tmpInfo = getInfo(self.database[self.result])
                    self.age = tmpInfo['age']
                    self.gender = tmpInfo['gender']
                    self.result = None
                except:
                    self.result = None
                    print('cannot read result image')


    '''def redrawAll(self, screen):
        screen.blit(self.bg, (0, 0))
        self.gameObjects.draw(screen)
        font = pygame.font.SysFont('Comic Sa', 20)
        t = str(self.text)
        if len(t) > 15:
            t = t[len(t)-15:]
        url = font.render((t), 1, (0,0,0))
        textRect = url.get_rect()
        textRect.topleft = TEXT_POSITION
        screen.blit(url, textRect)
        #ideal
        if self.ideal != None:
            cx, cy = IDEAL_POSITION
            x, y = cx - self.ideal.get_width()/2, cy - self.ideal.get_height()/2
            screen.blit(self.ideal, (x,y))'''
    def redrawAll(self, screen):
        screen.blit(self.bg, (0, 0))
        self.gameObjects.draw(screen)
        smallFont = pygame.font.SysFont('Comic San', 20)
        largeFont = pygame.font.SysFont('Comic San', 27)
        t = str(self.text)
        if len(t) > 35:
            t = t[len(t)-35:]
        url = smallFont.render((t), 1, (0,0,0))
        textRect = url.get_rect()
        textRect.topleft = TEXT_POSITION
        screen.blit(url, textRect)
        #ideal
        if self.ideal != None:
            cx, cy = IDEAL_POSITION
            x, y = cx - self.ideal.get_width()/2, cy - self.ideal.get_height()/2
            screen.blit(self.ideal, (x,y))

        #result
        if self.resultImage != None:
            cx, cy = RESULT_POSITION
            x, y = cx - self.resultImage.get_width()/2, cy - self.resultImage.get_height()/2
            screen.blit(self.resultImage, (x,y))

        #Info
        if self.age != None and self.gender != None and self.confidence != None:
            info = largeFont.render('Gender: %s  Age: %s' % (str(self.gender), str(self.age)), 1, (0,0,0))
            infoRect = info.get_rect()
            infoRect.topleft = INFO_POSITION
            screen.blit(info, infoRect)
            confidence = largeFont.render('Match Percentage: %s' % str(self.confidence) + '%', 1, (0,0,0))
            confRect = confidence.get_rect()
            confRect.topleft = CONFIDENCE_POSITION
            screen.blit(confidence, confRect)
            #Contact
            if self.gender == 'male':
                contactInfo = 'Contact: andrew@gmail.com'
            else:
                contactInfo = 'Contact: angela@gmail.com'
            contact = largeFont.render(contactInfo, 1, (0,0,0))
            contRect = contact.get_rect()
            contRect.topleft = CONTACT_POSITION
            screen.blit(contact, contRect)

    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, width = WIDTH, height = HEIGHT, fps = 30, title = "QUICKDATE"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255,255,255)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self._keys = dict()

        self.init()
        #self.bgm.play(-1)
        run = True
        while run:
            time = clock.tick(self.fps)

            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    run = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()