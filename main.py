import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_rendering import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.objectrender = ObjectRendering(self)
        self.raycasting = Raycasting(self)
        #self.spriteobject = SpriteObject(self)
        #self.animatedsprite = AnimatedSprite(self)
        self.objecthadler = Objecthandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.objecthadler.update()
        self.weapon.update()
        #self.spriteobject.update()
        #self.animatedsprite.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps()}')

    def check_event(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.K_ESCAPE):
                pg.quit() 
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def draw(self):
        #self.screen.fill("black")
        self.objectrender.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()

game = Game()
if __name__ == "__main__":
    game.run()