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
PLAYER = 'sprites\bluebird-midflap.png'
BACKGROUND = 'sprites\background-day.png'
PIPE_GREEN = 'sprites\pipe-green.png'
PIPE_RED = 'sprites\pipe-red.png'

def welcomeScreen():
    # function to show welcome screen
    pass

if __name__ == "__main__":
    #my game will start here
    pygame.init() # initialize the pygame modules 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption(' Flappy bird with Susheeth using python') 
    GAME_SPRITES['numbers'] = (pygame.image.load('sprites\0.png').convert_alpha(), 
                                pygame.image.load('sprites\1.png').convert_alpha(), 
                                pygame.image.load('sprites\2.png').convert_alpha(), 
                                pygame.image.load('sprites\3.png').convert_alpha(), 
                                pygame.image.load('sprites\4.png').convert_alpha(), 
                                pygame.image.load('sprites\5.png').convert_alpha(), 
                                pygame.image.load('sprites\6.png').convert_alpha(), 
                                pygame.image.load('sprites\7.png').convert_alpha(), 
                                pygame.image.load('sprites\8.png').convert_alpha(), 
                                pygame.image.load('sprites\9.png').convert_alpha())
    
    
    GAME_SPRITES['message']= pygame.image.load('sprites\message.png').convert_alpha() # load the message image
    GAME_SPRITES['base']= pygame.image.load('sprites\base.png').convert_alpha() # load the base image
    GAME_SPRITES['pipe']= (
        
        pygame.transform.rotate(pygame.image.load('PIPE_RED').convert_alpha(), 180), # load the pipe image and rotate it
        pygame.image.load('PIPE_GREEN').convert_alpha()) # load the pipe image
    GAME_SPRITES['baground'] = pygame.image.load('BACKGROUND').convert_alpha() # load the background 
    GAME_SPRITES['player']= pygame.imaage.load('PLAYER').convert_alpha() # load the player image
    
    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio\die.wav') # load the die sound
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio\hit.wav') # load the hit sound
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio\point.wav') # load the point sound
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio\swoosh.wav') # load the swoosh sound
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio\wing.wav') # load the wing sound
    
    while True:
        welcomeScreen()
        maingame()
        
        
    
    