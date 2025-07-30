import pygame as pg
from settings import *
import math

class Raycasting:
    def __init__(self, game):
        self.game = game
        self.raycasting_result = []
        self.objects_to_render = []
        self.textures = self.game.objectrender.wall_texture

    def get_object_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.raycasting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(offset * (-SCALE + TEXTURE_SIZE), 0, SCALE, TEXTURE_SIZE)
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height //2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))


    def ray_cast(self):
        self.raycasting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - FOV + 0.0001
        for ray in range (NUM_RAYS):
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
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
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
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += depth_delta

            if depth_vert < depth_hor:
                depth = depth_vert
                texture = texture_vert
                y_vert %= 1
                if cos_a > 0:
                    offset = y_vert
                else:
                    offset = 1 - y_vert
            if depth_hor < depth_vert:
                depth = depth_hor
                texture = texture_hor
                x_hor %= 1
                if sin_a > 0:
                    offset = 1 - x_hor
                else:
                    offset = x_hor
            
            #pg.draw.line(self.game.screen, "yellow", (100 * ox, 100 * oy), (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            depth *= math.cos(self.game.player.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth + 0.001)

            #color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            #pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            self.raycasting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_object_to_render()
