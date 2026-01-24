import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR, LEVELS_COUNT
from src.views import GameView
from src.core.asset_registries import LevelPaths

class GameWindow(arcade.Window):
    """Главное окно игры, управляет переключением View"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)

        # Хранилище данных между View
        self.game_data = {
            'level': 0,
            'medals': 0,
            'melee_damage_modifier': 1,
            'range_damage_modifier': 1,
            'speed_modifier': 1
        }

        # TODO: сделать загрузку параметров из БД

        self.game_view = None

        self.load_level(self.get_current_level_path())
        self.switch_view_to_game_view()

    def get_current_level_path(self):
        paths = {
            0: LevelPaths.level_0,
            1: LevelPaths.level_1,
            2: LevelPaths.level_2,
            3: LevelPaths.level_3
        }

        return paths[self.game_data["level"]]

    def load_level(self, level_path: str):
        """Загрузить уровень"""
        self.game_view = GameView(self, level_path=level_path)

    def switch_view_to_game_view(self):
        """Переключить на game_view"""
        self.show_view(self.game_view)

    def finish_level(self):
        """Выполнять при заврешении уровня"""

        self.game_data["level"] += 1
        if self.game_data["level"] < LEVELS_COUNT:
            self.load_level(self.get_current_level_path())
        else:
            # TODO: Сделать завершение игры после последнего уровня
            print("[Победа]")
            exit(0)
        self.switch_view_to_game_view()

        # TODO: Сюда вставить сохранение прогресса


if __name__ == "__main__":
    game = GameWindow()
    arcade.run()