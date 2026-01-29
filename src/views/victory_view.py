import arcade
import arcade.gui
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class VictoryScreenView(arcade.View):
    def __init__(self, window):
        super().__init__(window)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        vbox = arcade.gui.UIBoxLayout()

        new_game_btn = arcade.gui.UIFlatButton(text="Новая игра", width=300, height=50, x=SCREEN_WIDTH // 2 - 150,
                                               y=SCREEN_HEIGHT // 2 + 30)
        replay_btn = arcade.gui.UIFlatButton(text="Повторить последний уровень", width=300, height=50,
                                             x=SCREEN_WIDTH // 2 - 150, y=SCREEN_HEIGHT // 2 - 30)

        self.enabled = True

        @new_game_btn.event("on_click")
        def on_new_game(event):
            self.on_new_game()

        @replay_btn.event("on_click")
        def on_replay(event):
            self.on_replay_level()

        vbox.add(new_game_btn)
        vbox.add(replay_btn)

        self.manager.add(new_game_btn)
        self.manager.add(replay_btn)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "ПОБЕДА!",
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.GOLD,
            50,
            anchor_x="center",
            bold=True
        )
        self.manager.draw()

    def on_new_game(self):
        if self.enabled:
            self.window.reset_progress()
            self.enabled = False

    def on_replay_level(self):
        if self.enabled:
            self.window.game_data["level"] -= 1
            self.window.load_level(self.window.get_current_level_path())
            self.window.switch_view_to_game_view()
            self.enabled = False
