"""
Чистая тестовая сцена c Player.
Взаимодействие через WASD + код.
"""

import _bootstrap

import arcade
from src.entities.player import Player
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.core.asset_registries import TexturePaths


class PlayerTestRoom(arcade.Window):
    def __init__(self, width=1280, height=720, title="BaseEntity Test"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.spite_list = arcade.SpriteList()

        # Одна тестовая сущность
        self.player = Player(
        )

        self.spite_list.append(self.player)

        self.player.center_x = width // 2
        self.player.center_y = height // 2
        self.player.name = "Player"

        # Таймер для авто-обновления
        self.update_timer = 0.0

        # Множество для обработки нажатий клавиш
        self.keys_pressed = set()

        # --- Место для тестового кода ---

    def on_draw(self):
        self.clear()

        self.spite_list.draw()

        # === ТЕКСТОВЫЙ UI ===
        text_x = 50
        text_y = self.height - 50

        # Заголовок
        arcade.draw_text(
            "PLAYER TEST",
            text_x, text_y,
            arcade.color.CYAN,
            20,
            bold=True
        )
        text_y -= 40

        # Основные статы
        arcade.draw_text(
            f"Имя: {self.player.name}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Здоровье: {self.player.current_health:.1f} / {self.player.max_health}",
            text_x, text_y,
            arcade.color.GREEN if self.player.is_alive else arcade.color.RED,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Мана: {self.player.current_mana:.1f} / {self.player.max_mana}",
            text_x, text_y,
            arcade.color.CYAN if self.player.current_mana > 0 else arcade.color.GRAY,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Урон: {self.player.damage}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Скорость: {self.player.speed}",
            text_x, text_y,
            arcade.color.WHITE,
            16
        )
        text_y -= 30

        # Движение
        arcade.draw_text(
            f"Движение X: {self.player.change_x}",
            text_x, text_y,
            arcade.color.YELLOW,
            16
        )
        text_y -= 30

        arcade.draw_text(
            f"Движение Y: {self.player.change_y}",
            text_x, text_y,
            arcade.color.YELLOW,
            16
        )
        text_y -= 30

        # Неуязвимость
        invincible_text = "ДА" if self.player.is_invincible else "нет"
        invincible_color = arcade.color.CYAN if self.player.is_invincible else arcade.color.LIGHT_GRAY

        arcade.draw_text(
            f"Неуязвим: {invincible_text}",
            text_x, text_y,
            invincible_color,
            16
        )
        text_y -= 30

        if self.player.is_invincible:
            arcade.draw_text(
                f"Таймер: {self.player.invincibility_timer:.1f}с",
                text_x, text_y,
                arcade.color.CYAN,
                16
            )
            text_y -= 30

        # Жива/мертва
        alive_text = "ЖИВА" if self.player.is_alive else "МЕРТВА"
        alive_color = arcade.color.GREEN if self.player.is_alive else arcade.color.RED

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
            f"Позиция: ({self.player.center_x:.0f}, {self.player.center_y:.0f})",
            text_x, text_y,
            arcade.color.LIGHT_GRAY,
            14
        )

    def on_update(self, delta_time):
        # Обновляем движение игрок по нажатиям клавиш
        self.player.move_with_keys(self.keys_pressed)

        # Авто-обновление сущности
        self.spite_list.update()

        # --- Место для тествого кода ---

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


if __name__ == "__main__":
    testGame = PlayerTestRoom(SCREEN_WIDTH, SCREEN_HEIGHT,
                              "Ручной тест Player (взаимодействие через WASD + Space + код)")
    arcade.run()
