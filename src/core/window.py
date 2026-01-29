import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR, LEVELS_COUNT
from src.views import GameView, TutorialGameView, StartScreenView, DeathScreenView, VictoryScreenView, MenuView
from src.core.asset_registries import LevelPaths
from src.core.save_storage import init_db, load_game_data, save_game_data

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

        init_db()
        loaded_data = load_game_data()
        if loaded_data is not None:
            self.game_data.update(loaded_data)
        else:
            save_game_data(self.game_data)

        self.game_view = None
        self.start_screen_view = StartScreenView(self)
        self.death_screen_view = DeathScreenView(self)

        if self.game_data["level"] >= LEVELS_COUNT:
            self.switch_view_to_victory_screen_view()
        else:
            self.load_level(self.get_current_level_path())
            self.switch_view_to_start_screen_view()

        self.menu_opened = False

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

        # Грузим туториал отдельно
        if level_path == LevelPaths.level_0:
            self.game_view = TutorialGameView(self, level_path=level_path)
        else:
            self.game_view = GameView(self, level_path=level_path)


    def switch_view_to_game_view(self):
        """Переключить на game_view"""
        arcade.set_background_color(BACKGROUND_COLOR)
        self.show_view(self.game_view)
        self.menu_opened = False

    def switch_view_to_start_screen_view(self):
        """Переключить на start_screen_view"""
        arcade.set_background_color(arcade.color.BLACK)
        self.show_view(self.start_screen_view)
        self.menu_opened = False

    def switch_view_to_death_screen_view(self):
        """Переключить на death_screen_view"""
        arcade.set_background_color(arcade.color.BLACK)
        self.show_view(self.death_screen_view)
        self.menu_opened = False

    def switch_view_to_victory_screen_view(self):
        """Переключить на victory_screen_view"""
        arcade.set_background_color(arcade.color.BLACK)
        self.show_view(VictoryScreenView(self))
        self.menu_opened = False

    def switch_view_to_menu_view(self):
        """Переключить на menu_view"""

        sprite_lists = [
            self.game_view.ground_list,
            self.game_view.wall_list,
            self.game_view.finish_list,
            self.game_view.decoration_list,
            self.game_view.decoration_list_2,
            self.game_view.health_bottle_list,
            self.game_view.medals_list,
            self.game_view.spikes_list,
            self.game_view.enemies_list,
            self.game_view.player_list,
            self.game_view.additional_sprites,
            self.game_view.projectile_list,
            self.game_view.secret_walls_list
        ]

        world_camera = self.game_view.world_camera
        gui_camera = self.game_view.gui_camera

        self.show_view(MenuView(self, sprite_lists, world_camera, gui_camera))
        self.menu_opened = True

    def finish_level(self):
        """Выполнять при заврешении уровня"""

        self.game_data["level"] += 1
        self.game_data["medals"] = self.game_view.medals
        if self.game_data["level"] < LEVELS_COUNT:
            save_game_data(self.game_data)
            self.load_level(self.get_current_level_path())
            self.switch_view_to_start_screen_view()
        else:
            self.switch_view_to_victory_screen_view()

    def reset_progress(self):
        self.game_data = {
            'level': 0,
            'medals': 0,
            'melee_damage_modifier': 1,
            'range_damage_modifier': 1,
            'speed_modifier': 1
        }
        save_game_data(self.game_data)
        self.load_level(self.get_current_level_path())
        self.switch_view_to_game_view()
