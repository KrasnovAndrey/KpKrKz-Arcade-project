import arcade

from src.core.window import GameWindow
from src.views.game_view import GameView, TutorialGameView
from src.core.asset_registries import LevelPaths


class CheatState:
    def __init__(self):
        self.god_mode = False
        self.noclip = False
        self.speed_boost = False
        self.infinite_mana = False
        self.add_medals = 0


class CheatGameView(GameView):
    def __init__(self, window, cheats: CheatState, level_path: str = LevelPaths.test_level_2):
        self.cheats = cheats
        self.cheat_buttons = []
        super().__init__(window, level_path)

    def setup(self):
        super().setup()
        h = self.window.height
        x = 20
        w = 180
        bh = 28
        gap = 6
        y = h - 40
        self.cheat_buttons = [
            ("god_mode", x, y, w, bh),
            ("noclip", x, y - (bh + gap), w, bh),
            ("speed_boost", x, y - 2 * (bh + gap), w, bh),
            ("infinite_mana", x, y - 3 * (bh + gap), w, bh),
            ("add_medals", x, y - 4 * (bh + gap), w, bh),
            ("kill_enemies", x, y - 5 * (bh + gap), w, bh),
            ("finish_level", x, y - 6 * (bh + gap), w, bh),
        ]

        self.player.dash_duration *= 3
        self.player.dash_speed_multiplier *= 3

    def update_physics(self):
        for engine in self.physics_engines:
            engine.update()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.cheats.god_mode:
            self.player.current_health = self.player.max_health
            self.player.is_alive = True
        if self.cheats.infinite_mana:
            self.player.current_mana = self.player.max_mana
        if self.cheats.speed_boost:
            self.player.speed = self.player.original_speed * 2
        else:
            self.player.speed = self.player.original_speed
        if self.cheats.add_medals:
            self.medals += self.cheats.add_medals
            self.cheats.add_medals = 0

    def on_draw(self):
        super().on_draw()
        self.draw_cheat_panel()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        if key == arcade.key.SPACE:
            if self.player.change_x != 0 or self.player.change_y != 0:
                self.player.dash_cooldown_timer = 0
                self.player.dash()

    def draw_cheat_panel(self):
        for name, x, y, w, h in self.cheat_buttons:
            if name == "god_mode":
                active = self.cheats.god_mode
                label = "[G] God mode"
            elif name == "noclip":
                active = self.cheats.noclip
                label = "[N] Noclip"
            elif name == "speed_boost":
                active = self.cheats.speed_boost
                label = "[S] Speed x2"
            elif name == "infinite_mana":
                active = self.cheats.infinite_mana
                label = "[M] Infinite mana"
            elif name == "add_medals":
                active = False
                label = "[+] +100 medals"
            elif name == "kill_enemies":
                active = False
                label = "[K] Kill enemies"
            else:
                active = False
                label = "[F] Finish level"
            color = arcade.color.GREEN if active else arcade.color.RED
            arcade.draw_text(label, x, y + 6, color, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        for name, bx, by, bw, bh in self.cheat_buttons:
            if bx <= x <= bx + bw and by <= y <= by + bh:
                if name == "god_mode":
                    self.cheats.god_mode = not self.cheats.god_mode
                elif name == "noclip":
                    self.cheats.noclip = not self.cheats.noclip
                elif name == "speed_boost":
                    self.cheats.speed_boost = not self.cheats.speed_boost
                elif name == "infinite_mana":
                    self.cheats.infinite_mana = not self.cheats.infinite_mana
                elif name == "add_medals":
                    self.cheats.add_medals += 100
                elif name == "kill_enemies":
                    for enemy in list(self.enemies_list):
                        enemy.remove_from_sprite_lists()
                elif name == "finish_level":
                    self.window.finish_level()
                break


class TutorialCheatGameView(TutorialGameView, CheatGameView):
    def __init__(self, window, cheats: CheatState, level_path: str = LevelPaths.test_level_2):
        CheatGameView.__init__(self, window, cheats, level_path)


class CheatGameWindow(GameWindow):
    def __init__(self):
        self.cheats = CheatState()
        super().__init__()

    def load_level(self, level_path: str):
        if level_path == LevelPaths.level_0:
            self.game_view = TutorialCheatGameView(self, self.cheats, level_path=level_path)
        else:
            self.game_view = CheatGameView(self, self.cheats, level_path=level_path)


def main():
    game = CheatGameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
