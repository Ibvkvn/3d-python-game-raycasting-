from settings import *
from sprite_object import *
from npc import *

class Objecthandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_path = "resources/sprites/npc/"
        self.static_sprite_path = "resources/sprites/animated_sprites/green_sprite/"
        self.animated_sprite_path = "resources/sprites/animated_sprites/red_sprite/"
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        #add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, path=self.animated_sprite_path + "0.png", pos=(10.5, 3.5)))

        add_npc(NPC(game))

    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)