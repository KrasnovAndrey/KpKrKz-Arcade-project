import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR
from src.views import GameView
from src.core.asset_registries import LevelPaths

class GameWindow(arcade.Window):
    """Главное окно игры, управляет переключением View"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)

        # Хранилище данных между View
        self.game_data = {
            'level': 1,
            'medals': 0,
            'melee_damage_modifier': 1,
            'range_damage_modifier': 1,
            'speed_modifier': 1
        }

        # TODO: сделать загрузку параметров из БД

        self.game_view = None

        self.load_level(LevelPaths.test_level_2)
        self.switch_view_to_game_view()


    def load_level(self, level_path: str):
        """Загрузить уровень"""
        self.game_view = GameView(self, level_path=level_path)

    def switch_view_to_game_view(self):
        """Переключить на game_view"""
        self.show_view(self.game_view)


if __name__ == "__main__":
    game = GameWindow()
    arcade.run()