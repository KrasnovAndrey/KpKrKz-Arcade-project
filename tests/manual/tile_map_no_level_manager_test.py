import _bootstrap

import pyglet

pyglet.options["texture_min_filter"] = pyglet.gl.GL_NEAREST
pyglet.options["texture_mag_filter"] = pyglet.gl.GL_NEAREST

import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities import Player
from src.core.asset_registries import TexturePaths, LevelPaths

# Задаём размер окна
SCREEN_TITLE = "Tiled map load test"
TILE_SCALING = 1.0
CAMERA_LERP = 1.0


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color((118, 58, 54))

        self.keys_pressed = set()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

    def setup(self):
        # Создаём игрока
        self.player = Player(texture_path=TexturePaths.player, scale=TILE_SCALING)

        tile_map = arcade.load_tilemap(LevelPaths.test_level, scaling=TILE_SCALING)

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.collision_list = tile_map.sprite_lists["collision"]
        self.wall_list = tile_map.sprite_lists["walls"]
        self.ground_list = tile_map.sprite_lists["ground"]
        self.start_list = tile_map.sprite_lists["start"]

        self.tile_map = tile_map

        self.world_width = int(self.tile_map.width * self.tile_map.tile_width * TILE_SCALING)
        self.world_height = int(self.tile_map.height * self.tile_map.tile_height * TILE_SCALING)

        # Создаём физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.collision_list
        )

        self.spawn_player()

    def find_start_coordinates(self):
        start = self.start_list[0]
        return start.center_x, start.center_y

    def spawn_player(self):
        x, y = self.find_start_coordinates()
        self.player.center_x = x
        self.player.center_y = y

    def on_update(self, delta_time):
        # Обновляем физический движок
        self.physics_engine.update()

        # Обновляем движение игрока
        self.player_list.update()
        self.player.move_with_keys(self.keys_pressed)

        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            CAMERA_LERP,  # Плавность следования камеры
        )


    def on_draw(self):
        """Отрисовка всех спрайтов"""
        self.clear()

        self.world_camera.use()

        self.ground_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)



def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()