import random # for random number generation
import sys # for exit 
import pygame # for pygame library
from pygame.locals import * # basic py games import 

#global variables for the game 
FPS = 60 # frames per second
SCREEN_WIDTH = 290
SCREEN_HEIGHT = 520
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # screen size
GROUNDY = SCREEN_HEIGHT * 0.8 # ground height
GAME_SPRITES = {} # game sprites
GAME_SOUNDS = {} # game sounds
PLAYER = 'sprites/bluebird-midflap.png'
BACKGROUND = 'sprites/background-day.png'
PIPE_GREEN = 'sprites/pipe-green.png'
PIPE_RED = 'sprites/pipe-red.png'

def welcomeScreen():
    # function to show welcome screen
    playerx = int(SCREEN_WIDTH/5) # player x position
    playery = int(SCREEN_WIDTH - GAME_SPRITES['player'].get_height())/2 # player y position
    messagex = int((SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2) # message x position
    messagey = int(SCREEN_HEIGHT * 0.13) # message y position
    basex = 0 # base x position
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['baground'], (0, 0)) # draw the background
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey)) # draw the message
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY)) # draw the base
                pygame.display.update() # update the display
                FPSCLOCK.tick(FPS) # set the frames per second
                
    pass
def maingame():
    score = 0
    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_WIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREEN_WIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREEN_WIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or \
   (event.type == MOUSEBUTTONDOWN):  # This allows tap or mouse click
            
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['baground'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREEN_WIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREEN_HEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT/3
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe


    
if __name__ == "__main__":
    #my game will start here
    pygame.init() # initialize the pygame modules 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption(' Flappy bird with Susheeth using python') 
    GAME_SPRITES['numbers'] = (pygame.image.load('sprites/0.png').convert_alpha(), 
                                pygame.image.load('sprites/1.png').convert_alpha(), 
                                pygame.image.load('sprites/2.png').convert_alpha(), 
                                pygame.image.load('sprites/3.png').convert_alpha(), 
                                pygame.image.load('sprites/4.png').convert_alpha(), 
                                pygame.image.load('sprites/5.png').convert_alpha(), 
                                pygame.image.load('sprites/6.png').convert_alpha(), 
                                pygame.image.load('sprites/7.png').convert_alpha(), 
                                pygame.image.load('sprites/8.png').convert_alpha(), 
                                pygame.image.load('sprites/9.png').convert_alpha())
    
    
    GAME_SPRITES['message']= pygame.image.load('sprites/message.png').convert_alpha() # load the message image
    GAME_SPRITES['base']= pygame.image.load('sprites/base.png').convert_alpha() # load the base image
    GAME_SPRITES['pipe']= (
        
        pygame.transform.rotate(pygame.image.load(PIPE_RED).convert_alpha(), 180), # load the pipe image and rotate it
        pygame.image.load(PIPE_GREEN).convert_alpha()) # load the pipe image
    GAME_SPRITES['baground'] = pygame.image.load(BACKGROUND).convert_alpha() # load the background 
    GAME_SPRITES['player']= pygame.image.load(PLAYER).convert_alpha() # load the player image
    
    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav') # load the die sound
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav') # load the hit sound
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav') # load the point sound
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav') # load the swoosh sound
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav') # load the wing sound
    
    while True:
        welcomeScreen()
        maingame()
        
        
    
    