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

        arcade.draw_text(
            "Test Menu Text",
            self.window.width // 2,
            self.window.height // 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
            anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE and self.window.menu_opened:
            self.window.switch_view_to_game_view()
