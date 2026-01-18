from pyglet.event import EVENT_HANDLE_STATE

import _bootstrap

import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities import Player
from src.core.asset_registries import TexturePaths, LevelPaths
from src.entities import BaseEntity
from src.entities.enemies import BaseEnemy, Warrior
from src.entities.projectiles import BaseProjectile, MeleeAttack
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
        self.mouse_buttons_pressed = dict()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

    def setup(self):
        # Создаём игрока
        tile_map = arcade.load_tilemap(LevelPaths.test_level, scaling=TILE_SCALING)

        self.collision_list = tile_map.sprite_lists["collision"]
        self.wall_list = tile_map.sprite_lists["walls"]
        self.ground_list = tile_map.sprite_lists["ground"]
        self.start_list = tile_map.sprite_lists["start"]

        self.tile_map = tile_map

        self.world_width = int(self.tile_map.width * self.tile_map.tile_width * TILE_SCALING)
        self.world_height = int(self.tile_map.height * self.tile_map.tile_height * TILE_SCALING)

        self.projectile_list = arcade.SpriteList()

        self.base_entity = Warrior(projectiles_list=self.projectile_list)
        self.base_entity.center_x = 400
        self.base_entity.center_y = 400

        self.entity_list = arcade.SpriteList()
        self.entity_list.append(self.base_entity)

        self.player = Player(texture_path=TexturePaths.player, scale=TILE_SCALING, projectiles_list=self.projectile_list, enemies_list=self.entity_list)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.base_entity.set_player_list(self.player_list)

        # Создаём физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.collision_list,
        )

        self.collision_list_2 = self.collision_list = tile_map.sprite_lists["collision"]

        self.phycics_engine_2 = arcade.PhysicsEngineSimple(
            self.base_entity,
            self.collision_list_2
        )

        # Дополнительные спрайты игрока
        self.additional_sprites = arcade.SpriteList()
        self.additional_sprites.extend(self.player.setup_additional_sprites())
        self.additional_sprites.extend(self.base_entity.setup_additional_sprites())

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
        self.phycics_engine_2.update()

        # Обновляем движение игрока
        self.player_list.update()
        self.player.move_with_keys(self.keys_pressed)
        self.player.actions_with_mouse(self.mouse_buttons_pressed)

        self.entity_list.update()
        self.base_entity.update_detection(delta_time=delta_time)
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
            f"WarriorHp: {self.base_entity.current_health}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Warrior: {'Alive' if self.base_entity.is_alive else 'Dead'}",
            text_x, text_y,
            arcade.color.GREEN if self.base_entity.is_alive else arcade.color.RED,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"PlayerHp: {self.player.current_health}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Player: {'Alive' if self.player.is_alive else 'Dead'}",
            text_x, text_y,
            arcade.color.GREEN if self.player.is_alive else arcade.color.RED,
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

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_buttons_pressed[button] = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button in self.mouse_buttons_pressed:
            del self.mouse_buttons_pressed[button]

    def spawn_projectile(self):
        projectile = BaseProjectile(400, 200, direction=(random.choice((-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1)), 1), texture_path=TexturePaths.magic_ball,
                                    despawn_on_collision=True, hit_list=self.entity_list,
                                    obstacles_list=self.collision_list, speed=10)
        self.projectile_list.append(projectile)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
