from sprite_object import *
from random import randint, choice, random

class NPC(AnimatedSprite):
    def __init__(self, game, path="resources/sprites/npc/soldier/0.png", pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + "/attack")
        self.death_images = self.get_images(self.path + "/death")
        self.idle_images = self.get_images(self.path + "/idle")
        self.pain_images = self.get_images(self.path + "/pain")
        self.walk_images = self.get_images(self.path + "/walk")

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_casting = False
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.logic()
        #self.draw_raycast()

    def check_wall(self, x, y):
        return(x, y) not in self.game.map.world_map

    def check_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.player.map_pos
        next_x, next_y = next_pos
        angle = math.atan2(next_y + 0.5 -self.y, next_x + 0.5 - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.check_collision(dx, dy)

    def death_animation(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_npc(self):
        if self.raycast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health > 1:
            self.alive = False
            self.game.sound.npc_death.play()
            #self.animate(self.death_images)

    def logic(self):
        if self.alive:
            self.raycast_value = self.npc_raycasting()
            self.check_hit_npc()
            if self.pain:
                self.animate_pain()
            elif self.raycast_value:
                self.player_search_trigger = True
                self.animate(self.walk_images)
                self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.death_animation()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def npc_raycasting(self):
        if self.game.player.map_pos == self.map_pos:
            return True
        
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        if sin_a > 0:
            y_hor, dy = y_map + 1, 1
        else:
            y_hor, dy = y_map - 1e-6, -1

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPT):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        if cos_a > 0:
            x_vert, dx = x_map + 1, 1
        else:
            x_vert, dx = x_map -1e-6, -1

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        depth_delta = dx / cos_a
        dy = depth_delta * sin_a

        for i in range (MAX_DEPT):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break 
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += depth_delta
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False 
    
    def draw_raycast(self):
        pg.draw.circle(self.game.screen, "red", (100 * self.x, 100 * self.y), 15)
        #print(self.npc_raycasting())
        if self.npc_raycasting():
            #print("raycasting is True")
            pg.draw.line(self.game.screen, "orange", (100 * self.game.player.x, 100 * self.game.player.y), (100 * self.x, 100 * self.y), 2)