import arcade


class MenuView(arcade.View):
    def __init__(self, window, sprite_lists: arcade.SpriteList, world_camera: arcade.camera.Camera2D, gui_camera: arcade.camera.Camera2D):
        super().__init__(window)
        self.sprite_lists = sprite_lists
        self.world_camera = world_camera
        self.gui_camera = gui_camera
        self.mode = "menu"
        self.message = ""

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

        if self.mode == "menu":
            labels = [
                "Продолжить",
                "Новая игра",
                "Магазин",
                "Выйти",
            ]
        else:
            labels = [
                "Отхил (30)",
                "Усиление ближнего урона (40)",
                "Усиление дальнего урона (40)",
                "Скорость (40)",
                "Назад",
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

        if self.message:
            arcade.draw_text(
                self.message,
                center_x,
                center_y - total_height // 2 - 40,
                arcade.color.RED,
                16,
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

        if self.mode == "menu":
            labels = [
                "Продолжить",
                "Новая игра",
                "Магазин",
                "Выйти",
            ]
        else:
            labels = [
                "Отхил (30)",
                "Усиление ближнего урона (40)",
                "Усиление дальнего урона (40)",
                "Скорость (40)",
                "Назад",
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
                if self.mode == "menu":
                    if text == "Продолжить":
                        if self.window.menu_opened:
                            self.window.switch_view_to_game_view()
                    elif text == "Новая игра":
                        self.window.reset_progress()
                    elif text == "Магазин":
                        self.mode = "shop"
                        self.message = ""
                    elif text == "Выйти":
                        self.window.close()
                else:
                    if text == "Отхил (30)":
                        game_view = self.window.game_view
                        player = game_view.player
                        if game_view.medals >= 30 and player.current_health < player.max_health:
                            game_view.medals -= 30
                            player.current_health = player.max_health
                            self.message = ""
                        elif game_view.medals < 30:
                            self.message = "Недостаточно медалей"
                        else:
                            self.message = "Здоровье уже полное"
                    elif text == "Усиление ближнего урона (40)":
                        game_view = self.window.game_view
                        player = game_view.player
                        if game_view.medals >= 40:
                            game_view.medals -= 40
                            self.window.game_data["melee_damage_modifier"] *= 1.2
                            player.melee_damage *= 1.2
                            self.message = ""
                        else:
                            self.message = "Недостаточно медалей"
                    elif text == "Усиление дальнего урона (40)":
                        game_view = self.window.game_view
                        player = game_view.player
                        if game_view.medals >= 40:
                            game_view.medals -= 40
                            self.window.game_data["range_damage_modifier"] *= 1.2
                            player.range_damage *= 1.2
                            self.message = ""
                        else:
                            self.message = "Недостаточно медалей"
                    elif text == "Скорость (40)":
                        game_view = self.window.game_view
                        player = game_view.player
                        if game_view.medals >= 40:
                            game_view.medals -= 40
                            self.window.game_data["speed_modifier"] *= 1.2
                            player.original_speed *= 1.2
                            player.speed = player.original_speed
                            self.message = ""
                        else:
                            self.message = "Недостаточно медалей"
                    elif text == "Назад":
                        self.mode = "menu"
                        self.message = ""
                break
