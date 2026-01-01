"""
Измененная версия base_entity_test_room для проверки работы TexturePaths
"""

import arcade
from src.entities.base_entity import BaseEntity
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.core.asset_registries import TexturePaths


class BaseEntityTestRoom(arcade.Window):
    def __init__(self, width=1280, height=720, title="BaseEntity Test"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.spite_list = arcade.SpriteList()

        # Одна тестовая сущность
        self.entity = BaseEntity(
            max_health=100,
            damage=15,
            speed=3.0,
            texture_path=TexturePaths.player,
            scale=3
        )

        self.spite_list.append(self.entity)

        self.entity.center_x = width // 2
        self.entity.center_y = height // 2
        self.entity.name = "TestEntity"

        # Таймер для авто-обновления
        self.update_timer = 0.0

        # --- Место для тестового кода ---


    def on_draw(self):
        self.clear()

        self.spite_list.draw()

        # === ТЕКСТОВЫЙ UI ===
        text_x = 50
        text_y = self.height - 50

        # Заголовок
        arcade.draw_text(
            "BASE ENTITY TEST",
            text_x, text_y,
            arcade.color.CYAN,
            20,
            bold=True
        )
        text_y -= 40

        # Основные статы
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

    def on_update(self, delta_time):
        # Авто-обновление сущности
        self.spite_list.update()

        # --- Место для тествого кода ---


if __name__ == "__main__":
    testGame = BaseEntityTestRoom(SCREEN_WIDTH, SCREEN_HEIGHT,
                                  "Ручной тест BaseEntity (взаимодействие только через код)")
    arcade.run()
