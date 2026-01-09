import _bootstrap

import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities import Player
from src.core.asset_registries import TexturePaths, LevelPaths
from src.entities import BaseEntity
from src.entities.projectiles import BaseProjectile
import random

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

        self.base_entity = BaseEntity(max_health=20, invincibility_time=0)
        self.base_entity.center_x = 400
        self.base_entity.center_y = 400

        self.entity_list = arcade.SpriteList()
        self.entity_list.append(self.base_entity)

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

        # Дополнительные спрайты игрока
        self.additional_sprites = self.player.setup_additional_sprites()

        self.projectile_list = arcade.SpriteList()

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

        self.entity_list.update()
        self.projectile_list.update()

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
        self.entity_list.draw()
        self.player_list.draw()
        self.additional_sprites.draw()
        self.projectile_list.draw()

        text_x = -200
        text_y = 350
        arcade.draw_text(
            "PROJECTILE TEST",
            text_x, text_y,
            arcade.color.CYAN,
            20,
            bold=True
        )
        text_y -= 40

        arcade.draw_text(
            f"Press G to spawn projectile",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )

        text_y -= 30

        arcade.draw_text(
            f"BaseEntityHp: {self.base_entity.current_health}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"BaseEntity: {"Alive" if self.base_entity.is_alive else "Dead"}",
            text_x, text_y,
            arcade.color.GREEN if self.base_entity.is_alive else arcade.color.RED,
            16
        )
        text_y -= 30

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if arcade.key.G == key:
            self.spawn_projectile()

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def spawn_projectile(self):
        projectile = BaseProjectile(400, 200, direction=(random.randint(-1, 1), 1), texture_path=TexturePaths.magic_ball,
                                    despawn_on_collision=True, hit_list=self.entity_list,
                                    obstacles_list=self.collision_list, speed=10)
        self.projectile_list.append(projectile)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
