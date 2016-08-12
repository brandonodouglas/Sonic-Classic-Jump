# Sprites for the platform game
import pygame as pg
from settings import *
import random
from random import choice, randrange
vec = pg.math.Vector2

class Spritesheet:
    # Class for loading and handling of sprites
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # Get image from spritesheet(?)
        image = pg.Surface((width,height))


        image.blit(self.spritesheet, (0,0), (x, y, width, height))

        # Scaling the image
        #image = pg.transform.scale(image, (54,78)) #54,78

        return image
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = player_layer
        self.groups = game.sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Character Animation
        self.walking = False
        self.jumping = False
        self.dashing = False # I.e figure of 8 run
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        #self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.pos = vec(40, height-50)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    # Animation
    def load_images(self):

        # Dashing
        self.dashing_frames = [self.game.spritesheet.get_image(558,32,31,35),
                               self.game.spritesheet.get_image(598, 31, 31, 37),
                               self.game.spritesheet.get_image(639, 31, 31, 36),
                               self.game.spritesheet.get_image(681, 32, 30, 35)]
        self.dashing_frames_l = []
        for frame in self.dashing_frames: # Right movement
            frame.set_colorkey(black)
            self.dashing_frames_l.append(pg.transform.flip(frame, True, False))
        # Standing


        self.standing_frames = [self.game.spritesheet.get_image(198,193,27,39)]
        self.standing_frames_r = []
        for frame in self.standing_frames:
            self.standing_frames_r.append(pg.transform.flip(frame, True, False))
        for frame in self.standing_frames:
            frame.set_colorkey(black)
            pass
        # Walking frames
        self.walk_frames_r = [self.game.spritesheet.get_image(182,35,25,37),
                                self.game.spritesheet.get_image(212, 35, 26, 37),
                            self.game.spritesheet.get_image(248, 34, 27, 38),
                            self.game.spritesheet.get_image(279, 34, 37, 38),
                            self.game.spritesheet.get_image(323, 34, 32, 38),
                            self.game.spritesheet.get_image(363, 34, 31, 38),
                            self.game.spritesheet.get_image(399, 35, 26, 37)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(black)

            self.walk_frames_l.append(pg.transform.flip(frame, True, False)) # Horizontal veritcal for true and false
        # Jump frames
        self.jumpA = [self.game.spritesheet.get_image(233, 200, 24, 32),
                      self.game.spritesheet.get_image(233, 200, 24, 32),
                      self.game.spritesheet.get_image(233, 200, 24, 32),
                      self.game.spritesheet.get_image(172, 153, 32, 29),
                      self.game.spritesheet.get_image(213, 152, 29, 30),
                      self.game.spritesheet.get_image(250, 152, 30, 30),
                      self.game.spritesheet.get_image(290, 152, 30, 30),
                      self.game.spritesheet.get_image(408, 203, 30, 30),
                      self.game.spritesheet.get_image(408, 203, 30, 30),
                      self.game.spritesheet.get_image(408, 203, 30, 30),
                      self.game.spritesheet.get_image(408, 203, 30, 30),
                      self.game.spritesheet.get_image(408, 203, 30, 30),
                      self.game.spritesheet.get_image(408, 203, 30, 30),
                      self.game.spritesheet.get_image(172, 153, 32, 29),
                      self.game.spritesheet.get_image(213, 152, 29, 30),
                      self.game.spritesheet.get_image(250, 152, 30, 30),
                      self.game.spritesheet.get_image(290, 152, 30, 300),
                      self.game.spritesheet.get_image(267, 206, 29, 27),
                      self.game.spritesheet.get_image(267, 206, 29, 27),
                      self.game.spritesheet.get_image(267, 206, 29, 27),
                      self.game.spritesheet.get_image(267, 206, 29, 27),
                      self.game.spritesheet.get_image(232, 200, 25, 32),
                      self.game.spritesheet.get_image(232, 200, 25, 32),
                      self.game.spritesheet.get_image(232, 200, 25, 32),
                      self.game.spritesheet.get_image(232, 200, 25, 32),
                      self.game.spritesheet.get_image(198, 193, 27, 39)]
        self.jumpA_l = []
        for frame in self.jumpA:
            frame.set_colorkey(black)
            self.jumpA_l.append(pg.transform.flip(frame, True, False))
        self.spring_image1 = self.game.spritesheet.get_image(200, 244, 24, 45)

        self.spring_image1 = pg.transform.scale(self.spring_image1, (54, 78))
        self.spring_image1.set_colorkey(black)

    def jump(self):
        # Jump if standing on a platform only
        self.rect.x += 2
        hits =  pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            self.game.jump_sound.play()
            self.vel.y = -20



    def update(self):
        self.animate()
        self.acc = vec(0,player_grav) #0.5 for gravity
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc
        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc
        # Friction rules
        self.acc.x += self.vel .x * player_friction
        # Equations of motion
        self.vel += self.acc # For sliding motion
        if abs(self.vel.x) < 0.1:
            self.temp = self.vel.x
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Wrap around screen
        if self.pos.x > width + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2:
            self.pos.x = width + self.rect.width/2
        self.rect.midbottom = self.pos


    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.y < -19:
            self.jumping = True
        if self.vel.y >= 0:
            self.jumping = False
        if self.jumping:
            if now - self.last_update > 50:  # ms
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumpA)
                bottom = self.rect.bottom
                if self.vel.x > 0:  # Positive for right direction
                    self.image = self.jumpA[self.current_frame]
                    self.image = pg.transform.scale(self.image, (54, 78))
                else:
                    self.image = self.jumpA_l[self.current_frame]
                    self.image = pg.transform.scale(self.image, (54, 78))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # For spring animatiom
        if self.vel.y >-60 and self.vel.y <-21:
            if self.vel.x > 0:

                    self.image = self.spring_image1
            else:
                self.image = pg.transform.flip(self.spring_image1, True, False)

        if abs(self.vel.x) >= 6:
            self.dashing = True
        else:
            self.dashing = False
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # Running/Dashing animation
        if self.dashing:

            if now - self.last_update > 100:  # ms
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.dashing_frames_l)
                bottom = self.rect.bottom

                if self.vel.x > 0:  # Positive for right direction
                    self.image = self.dashing_frames[self.current_frame]
                    self.image = pg.transform.scale(self.image, (54, 78))

                else:
                    self.image = self.dashing_frames_l[self.current_frame]
                    self.image = pg.transform.scale(self.image, (54, 78))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # Show walk animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0: # Positive for right direction
                    self.image = self.walk_frames_r[self.current_frame]
                    self.image = pg.transform.scale(self.image, (54, 78))

                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    self.image = pg.transform.scale(self.image, (54, 78))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # Show idle animation
        if not self.jumping and not self.walking and not self.dashing:
            if now - self.last_update > 270: # ms
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.image = pg.transform.scale(self.image, (54, 78))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # Improved collision
        self.mask = pg.mask.from_surface(self.image)
# Clouds
class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = cloud_layer
        self.groups = game.sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(44, 102, 42, 14)
        scale = randrange(50, 101) / 100
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (int(200* scale), int(50*scale)))

        # Spawn location
        self.rect.x = randrange(width/2)
        self.rect.y = randrange(-500, -50)
    def update(self):
        if self.rect.top > height * 2:
            self.kill()

# Floating Island Scenery
class Floatingisland(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = island_layer
        self.groups = game.sprites, game.island
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(579, 210, 189, 93)

        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (110, 50))

        # Spawn location
        self.rect.x = randrange(width - 200)
        self.rect.y = randrange(-500, -50)
    def update(self):
        if self.rect.top > height * 2:
            self.kill()
# Class for waterfall scenery
class Waterfall(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = waterfall_layer
        self.groups = game.sprites, game.waters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(['waterf'])
        self.last = 0
        self.current_frame = 0
        self.load_waterfall_images()
        self.image = self.waterfall_images[0]
        self.rect = self.image.get_rect()
        # Spawn location
        self.rect.x = width - 100
        self.rect.y = 0

    def update(self):
        self.water_animate()
    def load_waterfall_images(self):
        # Waterfall Game scenery
        self.waterfall_images = [self.game.spritesheet.get_image(2834, 370, 64, 304),
                                 self.game.spritesheet.get_image(2914, 370, 64, 304),
                                 self.game.spritesheet.get_image(2989, 370, 64, 304),
                                 self.game.spritesheet.get_image(3066, 370, 64, 304),
                                 self.game.spritesheet.get_image(3138, 370, 64, 304),
                                 self.game.spritesheet.get_image(3211, 370, 64, 304),
                                 self.game.spritesheet.get_image(3299, 370, 64, 304),
                                 self.game.spritesheet.get_image(3373, 370, 64, 304)
                                 ]
        for frame in self.waterfall_images:
            frame.set_colorkey(black)
            #self.waterfall_images[0] = pg.transform.scale(self.waterfall_images[0], (64, height))
    def water_animate(self):

        now = pg.time.get_ticks()
        if now - self.last > 50:  # ms
            self.last = now
            self.current_frame = (self.current_frame + 1) % len(self.waterfall_images)
            self.image = self.waterfall_images[self.current_frame]
            self.image = pg.transform.scale(self.image, (64, height))

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = platform_layer
        self.groups = game.sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(56,310,65,30)
                  ]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.image = pg.transform.scale(self.image, (200, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < spring_spawn_freq:
            Spring(self.game, self)
        if randrange(50) < ring_spawn_freq:
            Ringg(self.game, self)


class Spring(pg.sprite.Sprite): #
    def __init__(self, game, plat): # Platform to sit on
        self._layer = spring_layer
        self.groups = game.sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.plat = plat # The platform
        self.type = choice(['spring'])

        self.image = self.game.spritesheet.get_image(632, 156, 28, 16)
        self.image = pg.transform.scale(self.image, (56, 32))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

        self.rect.centerx = self.plat.rect.centerx # Place at center of platform
        self.rect.bottom = self.plat.rect.top + 3
    def update(self):

        self.rect.bottom = self.plat.rect.top + 3
        # For powerup sprites
        if not self.game.platforms.has(self.plat):
            self.kill()


class Ringg(pg.sprite.Sprite):  #
        def __init__(self, game, plat):  # Platform to sit on
            self._layer = ring_layer
            self.groups = game.sprites, game.powerups1
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.load_ring_images()
            self.plat = plat  # The platform
            self.current_frame = 0
            self.last = 0

            self.type = choice(['ring'])

            self.image = self.ring_images[0]
            self.image = pg.transform.scale(self.image, (27, 27))
            self.image.set_colorkey(black)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.plat.rect.centerx  # Place at center of platform
            self.rect.bottom = self.plat.rect.top + 3

        def update(self):
            self.animate()
            self.rect.bottom = self.plat.rect.top + 3

            if not self.game.platforms.has(self.plat):
                self.kill()
            #If platform has a spring, kill

        def load_ring_images(self):
            self.ring_images = [self.game.spritesheet.get_image(459, 269, 16, 16),
                                self.game.spritesheet.get_image(479, 269, 12, 16),
                                self.game.spritesheet.get_image(494, 269, 6, 16),
                                self.game.spritesheet.get_image(512, 269, 12, 16),
                                self.game.spritesheet.get_image(528, 269, 16, 16)]

            for frame in self.ring_images:
                frame.set_colorkey(black)

        def animate(self):
            now = pg.time.get_ticks()
            if now - self.last > 50:  # ms
                self.last = now
                self.current_frame = (self.current_frame + 1) % len(self.ring_images)
                self.image = self.ring_images[self.current_frame]
                self.image = pg.transform.scale(self.image, (27, 27))


# I.e. the badniks / enemies
class Mob(pg.sprite.Sprite): #
    def __init__(self, game): # Platform to sit on
        self._layer = mob_layer
        self.groups = game.sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(256, 484,23,37)
        self.image = pg.transform.scale(self.image, (54, 78))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, width + 100])
        self.vx= randrange(1,4)
        if self.rect.centerx> width:
            self.vx *= -1
        self.rect.y = randrange(height/2)
        self.vy = 0
        self.dy = 0.5




    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > width + 100 or self.rect.right <-100:
            self.kill()
class Startscreen(pg.sprite.Sprite):
    def __init__(self, game,x,y,):
        self._layer = start_layer
        self.groups = game.sprites, game.startGui
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.startImage
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.pos = vec(40, height - 50)






