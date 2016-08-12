#Sonic platform game - main code
import pygame as pg
import random
import os
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # Initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)

        self.clock = pg.time.Clock()
        self.running = True
        self.my_font_name = pg.font.match_font(font_name)
        self.load_data()

    def load_data(self):


        # Load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, hs_file), 'w') as file:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # Load spritesheets image
        self.spritesheet = Spritesheet(path.join(img_dir, spritesheet))
        # Load icon

        # self.icon = Spritesheet(path.join(img_dir, logoimg))
        self.a = self.spritesheet.get_image(335, 154, 32, 32)
        self.a.set_colorkey(black)

        #self.a = self.screen
        #self.icon = pg.Surface((10,10))
        pg.display.set_icon(self.a)
        # Load sounds / music
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump.ogg'))
        self.spring_sound = pg.mixer.Sound(path.join(self.snd_dir, 'spring.ogg'))
        self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, 'death.ogg'))
        self.intro_sound = pg.mixer.Sound(path.join(self.snd_dir, 'coderforfunintro_jingle.ogg'))
        self.water_sound = pg.mixer.Sound(path.join(self.snd_dir, 'waterfall_splash.ogg'))
        self.eggman_sound = pg.mixer.Sound(path.join(self.snd_dir, 'eggman.ogg'))
        self.ring_sound = pg.mixer.Sound(path.join(self.snd_dir, 'ring.ogg'))


        # Start screen Decals
        self.start_decal = self.spritesheet.get_image(2300, 292, width, height)
        self.start_decal = pg.transform.scale(self.start_decal, (width, height))
        self.start_decal.set_colorkey(black)
        # Player decals
        self.sonic_springjump = self.spritesheet.get_image(200, 244, 24, 45)
        #self.start_decal = pg.transform.scale(self.start_decal, (width, height))
        self.sonic_springjump.set_colorkey(black)
        # Game over deals
        self.go_decal = self.spritesheet.get_image(874, 181, 142, 15)
        self.go_decal = pg.transform.scale(self.go_decal, (284, 30))
        self.go_decal.set_colorkey(black)
        self.go_screen_decals = self.spritesheet.get_image(1171,390,123,130)
        self.go_screen_decals = pg.transform.scale(self.go_screen_decals, (284, 260))
        self.go_screen_decals.set_colorkey(black)
        # Game scenery / background decals
        self.gamebg_top = self.spritesheet.get_image(1840, 73, 258, 119)
        #self.gamebg_top = pg.transform.scale(self.gamebg_top, (width, int(height/4)))
        self.gamebg_top.set_colorkey(black)
        self.gamebg_bottom = self.spritesheet.get_image(1586, 183, 266, 143)
        #self.gamebg_bottom = pg.transform.scale(self.gamebg_bottom, (width, int(height / 4)))
        self.gamebg_bottom.set_colorkey(black)
        # Eggman mob
        self.eggman = self.spritesheet.get_image(1142, 752, 77, 50)
        self.eggman = pg.transform.scale(self.eggman, (154, 100))
        self.eggman.set_colorkey(black)
        # Game Ui
        self.gameui = self.spritesheet.get_image(176, 398, 41, 31)
        self.gameui = pg.transform.scale(self.gameui, (82, 62))
        self.gameui.set_colorkey(black)
        #Icon


    def new(self):
        # Start a new game
        self.score = 0
        self.rings = 0
        self.ring_bonus = 0
        self.egg_freq = 500

        self.sprites = pg.sprite.LayeredUpdates()  # For layer ordering
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.powerups1 = pg.sprite.Group()

        self.waters = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.island = pg.sprite.Group()
        self.waterfall = Waterfall(self)
        self.startGui= pg.sprite.Group()
        self.player = Player(self)

        for plat in platform_list:
            Platform(self, *plat)
        self.mob_timer = 0
        self.egg_timer = 0

        self.last = 0
        self.island_timer = 0
        self.last1 = 0
        self.current_frame = 0



        pg.mixer.music.load(path.join(self.snd_dir, 'greenhillzone.ogg'))





        for i in range(4):
            c = Cloud(self)
            c.rect.y += 500


        self.run()

    def run(self):
        # Game Loop





        pg.mixer.music.play(loops=-1)




         # -1 infinite repeat
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)


            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500) # Stop music when game stops running


    def update(self):
        #print(self.player.vel.y)

        # Game Loop - update

        self.sprites.update()

        self.wait()
        # Spawn a mob?
        now = pg.time.get_ticks()



        # Eggman boss code
        if now - self.mob_timer > 1550 + random.choice([-1000,-500,0,500,1000]):
            self.mob_timer = now
            if len(self.mobs) == 0: # To only show one mob on the screen at a time.
                self.bee = Mob(self)
        if now - self.egg_timer > 500: # Waits for 40 seconds
            self.egg_timer = now

            if len(self.mobs) == 0:  # To only show one mob on the screen at a time.
                self.eggmanM = Mob(self)
                self.eggman_sound.play()

                if self.eggmanM.vx < 0:
                    self.eggmanM.image = self.eggman
                else:
                    self.eggmanM.image = pg.transform.flip(self.eggman, True, False)









            #self.boss1.fadeout(500)







        # Island handling
        #Hit water?
        water_hits = pg.sprite.spritecollide(self.player, self.waters, False)

        for waterf in water_hits:
            if waterf.type == 'waterf':
                self.water_sound.play()








        # Hit mob?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.player.image = self.spritesheet.get_image(397, 246,34,43)
            self.player.image = pg.transform.scale(self.player.image, (54, 78))
            self.player.image.set_colorkey(black)
            # Show game over


            self.death_sound.play()
            self.playing = False




        # Check of player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10: # Stops the standing in air bug

                    if self.player.pos.y < lowest.rect.centery: # Only snap if players feet is higher than bottom of platform
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
        # SCROLLING SCREEN
        # if player reacher top quarter of screen..
        if self.player.rect.top <= height / 4:
            if random.randrange(100) < 3:
                # Spawn a cloud
                Cloud(self)
            # Spawn a floating island
            if self.player.rect.top <= height / 4:
                if random.randrange(120) < 1:
                    # Spawn a cloud
                    Floatingisland(self)
            # MOVE PLATFORM AND PLAYER DOWN


            self.player.pos.y += max(abs(self.player.vel.y),2)  # upwards vel is negavtive, we need down
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y /2 ), 2) # Move clouds down
            for island in self.island:
                island.rect.y += max(abs(self.player.vel.y / 2), 1.5)
            for mob in self.mobs:  # move all platforms down at same rate
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms: #move all platforms down at same rate
                plat.rect.y += max(abs(self.player.vel.y),2) #to move upwards
                if plat.rect.top >= height: # If platform is off screen, remvoe it, save processing power
                    plat.kill()
                    self.score += 10
        # If player hits spring
        spring_hits = pg.sprite.spritecollide(self.player, self.powerups, True)

        for spring in spring_hits:
            if spring.type == 'spring':
                self.spring_sound.play()

                self.player.vel.y = -spring_power
                #self.player.image = self.sonic_springjump
                self.player.jumping = False
        # If player collects ring
        ring_hits = pg.sprite.spritecollide(self.player, self.powerups1, True)
        for ring in ring_hits:

            if ring.type == 'ring':
                # Change self.ring.image...
                self.rings += 1
                self.score += 5
                self.ring_bonus += 5
                self.ring_sound.play()



        #print(self.rings)



        # Death condition + animation
        if self.player.rect.bottom > height:
            for spr in self.sprites: # Move everying up animation
                spr.rect.y -= max(self.player.vel.y, 10)
                if spr.rect.bottom < 0:
                    spr.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # Spawn new platforms to keep average number of platforms
        while len(self.platforms) < 6:
            WIDTH = random.randrange(50,100)
            #using x,y,w,h format
            Platform(self, random.randrange(0,width-WIDTH),
                    random.randrange(-75, -30))


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:

                    self.player.jump()





    def draw(self):

        # Game Loop - draw
        if self.waiting == False:
            time = pg.time.get_ticks()

        self.screen.fill(blue)



        self.sprites.draw(self.screen)




        # Scenery images


        self.border = self.screen.blit(self.gamebg_bottom, (0, height - 143))
        self.screen.blit(self.gamebg_top, (width-258, 0))
        # Game ui
        self.screen.blit(self.gameui, (25, 50))
        self.draw_text(str(self.score), 30, white, 140, 41)
        self.draw_text(str(self.rings),30,white, 140, 81)

        if self.playing == False:
            # Show game over thing
            self.screen.blit(self.go_decal, (width/2-150, height/2 - 30))


        pg.display.flip()



    def show_start_screen(self):
        # Show the Start Screen
        self.screen.blit(self.start_decal, (0, 0))
        self.draw_text("Use the arrow keys to play!", 15, white, width / 4 + 30, 380)
        pg.mixer.music.load(path.join(self.snd_dir, 'titletheme.ogg'))
        pg.mixer.music.play(loops=0)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)


    def show_go_screen(self):
        self.screen.fill(black)
        self.screen.blit(self.go_screen_decals, (width / 2 - 150, height / 2 - 200))

        if self.running == False: # exit
            return
        self.draw_text("Score: " + str(self.score),22,white,width/2,height/2 + 50)
        self.draw_text("RING BONUS: " + str(self.ring_bonus),22,yellow,width/2,height/2 + 130)
        self.draw_text("Press the p key to play again",22, white, width/2, height * 0.75 + 50)
        if self.score > self.highscore:
            pg.mixer.music.load(path.join(self.snd_dir, 'jingle.ogg'))
            pg.mixer.music.play(loops=0)
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE! ",22,red, width/2,height/2 + 90)
            with open(path.join(self.dir, hs_file), 'w') as file:
                file.write(str(self.score))
        else:
            pg.mixer.music.load(path.join(self.snd_dir, 'gameover.ogg'))
            pg.mixer.music.play(loops=0)

            self.draw_text("High score: " + str(self.highscore), 22, red, width / 2, height/2 + 90)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_intro_screen(self):
        self.intro_sound.play(loops=0)
        self.draw_text("coderforfun", 30, green, width / 2, height / 2)
        pg.display.flip()
        self.wait()
        self.screen.fill(black)





                #self.waiting = False

    def wait(self):
        self.last = 0
        self.waiting = True
        while self.waiting:
            now = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.running = False


            if now - self.last > 4000:
                self.last = now
                self.waiting = False

    def wait_for_key(self):

        self.waiting = True
        while self.waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:# if user presses key
                        self.waiting = False




    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.my_font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)








g = Game()
g.show_intro_screen()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()


pg.quit()
