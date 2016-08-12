# Game options/settings
title = "sonic game"
width = 480
height = 608
FPS = 60
font_name = 'arial'
hs_file = 'highscore.txt'
spritesheet = 'sonicsprites.png'
logoimg = 'soniclogo.png'
# Player properties
player_acc = 0.77
player_friction = -0.12
player_grav = 0.7
# Colours
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
blue =  (33,0,165)
red = (255,0,0)
yellow = (255,255,0)

# Power ups / game properties
spring_power = 60
spring_spawn_freq = 7
mob_freq = 5000 # ms
player_layer = 2
platform_layer = 1
spring_layer = 1
mob_layer = 2
cloud_layer = -1
island_layer = -1
waterfall_layer = 3
ring_layer = 0
ring_spawn_freq = 25




# Starting platforms
# (x,y,w,h) format
platform_list = [(0,height - 50),
                 (width/2 - 58, height * 0.75 - 50),
                 (125, height - 350),
                 (350, 200),
                 (175, 100)
                 ]