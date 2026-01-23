import arcade

from src.core.asset_registries import TexturePaths


class GameHUD:
    def __init__(self, window: arcade.Window):
        self.window = window

        self.full_heart_path = TexturePaths.ui_full_heart
        self.empty_heart_path = TexturePaths.ui_empty_heart

        self.full_mana_path = TexturePaths.ui_full_mana_ball
        self.empty_mana_path = TexturePaths.ui_empty_mana_ball

        self.medal_path = TexturePaths.ui_medal

        self.max_hearts = 10
        self.heart_size = 32
        self.icon_margin = 8

        self.max_mana = 10
        self.mana_size = 18

        self.currency_icon_size = 24

        self._hearts_sprites = arcade.SpriteList(use_spatial_hash=False)
        self._mana_sprites = arcade.SpriteList(use_spatial_hash=False)
        self._currency_sprites = arcade.SpriteList(use_spatial_hash=False)

    def display_health(self, value: int):
        if value < 0: # Кто так не делает, тому гореть в аду
            value = 0
        if value > self.max_hearts * 2:
            value = self.max_hearts * 2

        full_hearts = value // 2
        half_heart = value % 2

        start_x = self.icon_margin + self.heart_size / 2
        y = self.window.height - self.icon_margin - self.heart_size / 2

        self._hearts_sprites.clear()

        for i in range(self.max_hearts):
            x = start_x + i * (self.heart_size + 2)

            if i < full_hearts:
                texture_path = self.full_heart_path
            elif i == full_hearts and half_heart:
                texture_path = self.half_heart_path
            else:
                texture_path = self.empty_heart_path

            sprite = arcade.Sprite(texture_path)
            sprite.center_x = x
            sprite.center_y = y
            self._hearts_sprites.append(sprite)

        self._hearts_sprites.draw()

    def display_mana(self, value: int):
        if value < 0:
            value = 0
        if value > self.max_mana:
            value = self.max_mana

        start_x = self.icon_margin + self.mana_size / 2
        y = self.window.height - self.icon_margin - self.heart_size - self.icon_margin - self.mana_size / 2

        self._mana_sprites.clear()

        for i in range(self.max_mana):
            x = start_x + i * (self.mana_size + 2)
            texture_path = self.full_mana_path if i < value else self.empty_mana_path

            sprite = arcade.Sprite(texture_path)
            sprite.center_x = x
            sprite.center_y = y
            self._mana_sprites.append(sprite)

        self._mana_sprites.draw()

    def display_currency(self, value: int):
        start_x = self.icon_margin + self.currency_icon_size / 2
        y = self.window.height - self.icon_margin - self.heart_size - self.icon_margin - self.mana_size - self.icon_margin - self.currency_icon_size / 2

        self._currency_sprites.clear()

        sprite = arcade.Sprite(self.medal_path)
        sprite.center_x = start_x
        sprite.center_y = y
        self._currency_sprites.append(sprite)

        self._currency_sprites.draw()

        text_x = start_x + self.currency_icon_size / 2 + self.icon_margin
        text_y = y - self.currency_icon_size / 4

        arcade.draw_text(str(value), text_x, text_y, arcade.color.WHITE, 16)
