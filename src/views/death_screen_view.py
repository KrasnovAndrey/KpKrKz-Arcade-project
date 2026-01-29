import arcade


class DeathScreenView(arcade.View):
    def __init__(self, window):
        super().__init__(window)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "ВЫ УМЕРЛИ",
            self.window.width // 2,
            self.window.height // 2 + 30,
            arcade.color.INDIAN_RED,
            40,
            anchor_x="center",
            anchor_y="center",
        )

        arcade.draw_text(
            "Нажмите Enter чтобы возродиться",
            self.window.width // 2,
            self.window.height // 2 - 30,
            arcade.color.WHITE,
            30,
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.on_enter_press()

    def on_enter_press(self):
        self.window.switch_view_to_game_view()