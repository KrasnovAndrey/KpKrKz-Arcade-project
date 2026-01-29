import arcade


class MenuView(arcade.View):
    def __init__(self, window, sprite_lists: arcade.SpriteList, world_camera: arcade.camera.Camera2D, gui_camera: arcade.camera.Camera2D):
        super().__init__(window)
        self.sprite_lists = sprite_lists
        self.world_camera = world_camera
        self.gui_camera = gui_camera

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        for sprite_list in self.sprite_lists:
            sprite_list.draw()

        self.gui_camera.use()

        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                self.window.width // 2,
                self.window.height // 2,
                self.window.width,
                self.window.height,
            ),
            (0, 0, 0, 180)
        )

        center_x = self.window.width // 2
        center_y = self.window.height // 2
        button_width = 260
        button_height = 50
        gap = 20

        labels = [
            "Продолжить",
            "Новая игра",
            "Магазин",
            "Выйти",
        ]

        total_height = len(labels) * button_height + (len(labels) - 1) * gap
        start_y = center_y + total_height // 2 - button_height // 2

        for index, text in enumerate(labels):
            y = start_y - index * (button_height + gap)
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    center_x,
                    y,
                    button_width,
                    button_height,
                ),
                (50, 50, 80, 230)
            )
            arcade.draw_text(
                text,
                center_x,
                y,
                arcade.color.WHITE,
                20,
                anchor_x="center",
                anchor_y="center",
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE and self.window.menu_opened:
            self.window.switch_view_to_game_view()

    def on_mouse_press(self, x, y, button, modifiers):
        center_x = self.window.width // 2
        center_y = self.window.height // 2
        button_width = 260
        button_height = 50
        gap = 20

        labels = [
            "Продолжить",
            "Новая игра",
            "Магазин",
            "Выйти",
        ]

        total_height = len(labels) * button_height + (len(labels) - 1) * gap
        start_y = center_y + total_height // 2 - button_height // 2

        for index, text in enumerate(labels):
            y_button = start_y - index * (button_height + gap)
            left = center_x - button_width / 2
            right = center_x + button_width / 2
            bottom = y_button - button_height / 2
            top = y_button + button_height / 2

            if left <= x <= right and bottom <= y <= top:
                if text == "Продолжить":
                    if self.window.menu_opened:
                        self.window.switch_view_to_game_view()
                elif text == "Выйти":
                    self.window.close()
                break
