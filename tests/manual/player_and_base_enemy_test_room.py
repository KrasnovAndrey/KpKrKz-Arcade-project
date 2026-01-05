"""
Измененная версия base_entity_test_room для проверки работы TexturePaths
"""

import _bootstrap

import arcade

from src.entities import Player
from src.entities.enemies import BaseEnemy
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.core.asset_registries import TexturePaths


class BaseEntityTestRoom(arcade.Window):
    def __init__(self, width=1280, height=720, title="BaseEntity Test"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.player_list = arcade.SpriteList()
        self.player = Player(texture_path=TexturePaths.player, scale=5)
        self.player_list.append(self.player)

        self.player.center_x = width // 4
        self.player.center_y = height // 2
        self.player.name = "Player"

        self.enemy_list = arcade.SpriteList()
        self.enemy = BaseEnemy()
        self.enemy_list.append(self.enemy)

        self.enemy.center_x = int(width * 3/4)
        self.enemy.center_y = height // 2
        self.enemy.name = "Enemy"

        self.keys_pressed = set()


        # Таймер для авто-обновления
        self.update_timer = 0.0

        # --- Место для тестового кода ---


    def on_draw(self):
        self.clear()

        self.player_list.draw()
        self.enemy_list.draw()

        # === ТЕКСТОВЫЙ UI ===
        text_x = 50
        text_y = self.height - 50

        # Заголовок
        arcade.draw_text(
            "PLAYER + BASE ENEMY",
            text_x, text_y,
            arcade.color.CYAN,
            20,
            bold=True
        )
        text_y -= 40

        arcade.draw_text(
            f"{self.enemy.name}: {"Вижу игрока" if self.enemy.player_detected else "Не вижу игрока"}",
            text_x, text_y,
            arcade.color.GREEN if self.enemy.player_detected else arcade.color.RED,
            16
        )


        """
        arcade.draw_text(
            f"Имя: {self.entity.name}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Здоровье: {self.entity.current_health:.1f} / {self.entity.max_health}",
            text_x, text_y,
            arcade.color.GREEN if self.entity.is_alive else arcade.color.RED,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Урон: {self.entity.damage}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Скорость: {self.entity.speed}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        # Движение
        arcade.draw_text(
            f"Движение X: {self.entity.change_x}",
            text_x, text_y,
            arcade.color.YELLOW,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Движение Y: {self.entity.change_y}",
            text_x, text_y,
            arcade.color.YELLOW,
            16
        )
        text_y -= 30

        # Неуязвимость
        invincible_text = "ДА" if self.entity.is_invincible else "нет"
        invincible_color = arcade.color.CYAN if self.entity.is_invincible else arcade.color.LIGHT_GRAY

        arcade.draw_text(
            f"Неуязвим: {invincible_text}",
            text_x, text_y,
            invincible_color,
            16
        )
        text_y -= 30

        if self.entity.is_invincible:
            arcade.draw_text(
                f"Таймер: {self.entity.invincibility_timer:.1f}с",
                text_x, text_y,
                arcade.color.CYAN,
                16
            )
            text_y -= 30

        # Жива/мертва
        alive_text = "ЖИВА" if self.entity.is_alive else "МЕРТВА"
        alive_color = arcade.color.GREEN if self.entity.is_alive else arcade.color.RED

        arcade.draw_text(
            f"Состояние: {alive_text}",
            text_x, text_y,
            alive_color,
            16,
            bold=True
        )
        text_y -= 40

        # Позиция
        arcade.draw_text(
            f"Позиция: ({self.entity.center_x:.0f}, {self.entity.center_y:.0f})",
            text_x, text_y,
            arcade.color.LIGHT_GRAY,
            14
        )
    """

    def on_update(self, delta_time):
        # Движение игрока по клавишам
        self.player.move_with_keys(self.keys_pressed)

        # Обновления обнаружения игрока врагом
        self.enemy.update_detection(self.player_list, delta_time)

        # Авто-обновление сущностей
        self.player_list.update()
        self.enemy_list.update()

        # --- Место для тествого кода ---

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


if __name__ == "__main__":
    testGame = BaseEntityTestRoom(SCREEN_WIDTH, SCREEN_HEIGHT,
                                  "Ручной тест Player + BaseEnemy")
    arcade.run()
