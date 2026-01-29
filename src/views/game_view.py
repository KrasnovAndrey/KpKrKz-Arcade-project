import arcade
from arcade import draw_text

from src.core.asset_registries import LevelPaths, TexturePaths
from src.constants import TILE_SCALING, BACKGROUND_COLOR, CAMERA_LERP, SPIKES_DAMAGE, HEALTH_PER_HEALTH_BOTTLE
from src.entities import Player
from src.entities.enemies import Warrior, Barbarian, Archer
from src.ui import GameHUD
from pyglet.graphics import Batch


class GameView(arcade.View):
    def __init__(self, window, level_path: str = LevelPaths.test_level_2):
        super().__init__(window)
        self.level_path = level_path

        self.keys_pressed = set()
        self.mouse_buttons_pressed = dict()
        self.medals = self.window.game_data["medals"]

        self.level_finished = False

        self.setup()

    def setup(self):
        """Инициализация или переинициализация"""
        self.tile_map = arcade.load_tilemap(self.level_path, scaling=TILE_SCALING)

        arcade.set_background_color(BACKGROUND_COLOR)

        self.collision_list = self.tile_map.sprite_lists["Collision"]
        self.wall_list = self.tile_map.sprite_lists["Walls"]
        self.ground_list = self.tile_map.sprite_lists["Ground"]
        self.start_list = self.tile_map.sprite_lists["Start"]
        self.finish_list = self.tile_map.sprite_lists["Finish"]
        self.decoration_list = self.tile_map.sprite_lists["Decorations"]
        self.spikes_list = self.tile_map.sprite_lists["Spikes"]
        self.spikes_list = self.tile_map.sprite_lists["Spikes"]

        try:
            self.decoration_list_2 = self.tile_map.sprite_lists["Decorations2"]
        except KeyError:
            self.decoration_list_2 = arcade.SpriteList()

        try:
            self.secret_walls_list = self.tile_map.sprite_lists["SecretWalls"]
        except KeyError:
            self.secret_walls_list = arcade.SpriteList()

        try:
            self.health_bottle_list = self.tile_map.sprite_lists["HealthBottle"]
        except KeyError:
            self.health_bottle_list = arcade.SpriteList()

        self.physics_engines = []

        self.projectile_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.medals_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.additional_sprites = arcade.SpriteList()

        self.spawn_enemies()
        self.player = None
        self.spawn_player()

        self.spawn_medals()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.hud = GameHUD(window=self)

    def on_update(self, delta_time):
        self.update_physics()

        self.player_list.update()
        self.player.move_with_keys(self.keys_pressed)
        self.player.actions_with_mouse(self.mouse_buttons_pressed)

        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            CAMERA_LERP,
        )

        self.enemies_list.update()
        self.update_enemies_detection(delta_time)

        self.projectile_list.update()

        self.check_player_and_spikes_collision()
        self.check_player_and_medals_collision()
        self.check_player_and_health_bottles_collision()

        self.check_finish()

        if not self.player.is_alive:
            self.restart_level()


    def on_draw(self):
        self.clear()

        self.world_camera.use()

        self.ground_list.draw()
        self.wall_list.draw()
        self.finish_list.draw()
        self.decoration_list.draw()
        self.decoration_list_2.draw()
        self.health_bottle_list.draw()
        self.medals_list.draw()
        self.spikes_list.draw()
        self.enemies_list.draw()
        self.player_list.draw()
        self.additional_sprites.draw()
        self.projectile_list.draw()
        self.secret_walls_list.draw()

        self.gui_camera.use()
        self.hud.display_health(self.player.current_health)
        self.hud.display_mana(self.player.current_mana)
        self.hud.display_currency(self.medals)

    def spawn_enemies(self):
        self.spawn_warriors()
        self.spawn_barbarians()
        self.spawn_archers()

    def spawn_warriors(self):
        warriors_list = self.tile_map.sprite_lists["Warrior"]
        for enemy in warriors_list:
            warrior = Warrior(player_list=self.player_list, projectiles_list=self.projectile_list,
                              collision_list=self.collision_list)
            warrior.center_x = enemy.center_x
            warrior.center_y = enemy.center_y
            self.enemies_list.append(warrior)

            self.additional_sprites.extend(warrior.setup_additional_sprites())

            physics_engine = arcade.PhysicsEngineSimple(warrior, self.collision_list)
            self.physics_engines.append(physics_engine)

    def spawn_barbarians(self):
        barbarians_list = self.tile_map.sprite_lists["Barbarian"]
        for enemy in barbarians_list:
            barbarian = Barbarian(player_list=self.player_list, projectiles_list=self.projectile_list,
                                  collision_list=self.collision_list)
            barbarian.center_x = enemy.center_x
            barbarian.center_y = enemy.center_y
            self.enemies_list.append(barbarian)

            self.additional_sprites.extend(barbarian.setup_additional_sprites())

            physics_engine = arcade.PhysicsEngineSimple(barbarian, self.collision_list)
            self.physics_engines.append(physics_engine)

    def spawn_archers(self):
        archers_list = self.tile_map.sprite_lists["Archer"]
        for enemy in archers_list:
            archer = Archer(player_list=self.player_list, projectiles_list=self.projectile_list,
                            collision_list=self.collision_list)
            archer.center_x = enemy.center_x
            archer.center_y = enemy.center_y
            self.enemies_list.append(archer)

            self.additional_sprites.extend(archer.setup_additional_sprites())

            physics_engine = arcade.PhysicsEngineSimple(archer, self.collision_list)
            self.physics_engines.append(physics_engine)

    def spawn_player(self):
        start = self.tile_map.sprite_lists["Start"][0]
        x, y = start.center_x, start.center_y
        self.player = Player(enemies_list=self.enemies_list, projectiles_list=self.projectile_list,
                             collision_list=self.collision_list)

        self.player_list.append(self.player)

        self.player.center_x = x
        self.player.center_y = y

        melee_modifier = self.window.game_data.get("melee_damage_modifier", 1)
        range_modifier = self.window.game_data.get("range_damage_modifier", 1)
        speed_modifier = self.window.game_data.get("speed_modifier", 1)

        self.player.melee_damage *= melee_modifier
        self.player.range_damage *= range_modifier
        self.player.original_speed *= speed_modifier
        self.player.speed = self.player.original_speed

        self.additional_sprites.extend(self.player.setup_additional_sprites())

        physics_engine = arcade.PhysicsEngineSimple(self.player, self.collision_list)
        self.physics_engines.append(physics_engine)

    def spawn_medals(self):
        medals = self.tile_map.sprite_lists["Medals"]
        for sprite in medals:
            medal = arcade.Sprite(path_or_texture=arcade.load_texture(TexturePaths.ui_medal))
            medal.center_x = sprite.center_x
            medal.center_y = sprite.center_y
            self.medals_list.append(medal)

    def update_enemies_detection(self, delta_time: float):
        for enemy in self.enemies_list:
            enemy.update_detection(delta_time)

    def update_physics(self):
        for physics_engine in self.physics_engines:
            physics_engine.update()

    def check_player_and_spikes_collision(self):
        collision_list = arcade.check_for_collision_with_list(self.player, self.spikes_list)
        if collision_list:
            self.player.take_damage(SPIKES_DAMAGE)

    def check_player_and_medals_collision(self):
        collision_list = arcade.check_for_collision_with_list(self.player, self.medals_list)
        for medal in collision_list:
            self.medals += 1
            medal.remove_from_sprite_lists()

    def check_player_and_health_bottles_collision(self):
        collision_list = arcade.check_for_collision_with_list(self.player, self.health_bottle_list)
        if collision_list:
            self.player.heal(HEALTH_PER_HEALTH_BOTTLE)
            for bottle in collision_list:
                bottle.remove_from_sprite_lists()

    def check_finish(self):
        """Завершить уровень, когда игрок вошел в выход"""
        collision_list = arcade.check_for_collision_with_list(self.player, self.finish_list)
        if collision_list and not self.level_finished:
            self.window.finish_level()
            self.level_finished = True

    def restart_level(self):
        self.window.load_level(self.window.get_current_level_path())
        self.window.switch_view_to_death_screen_view()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE and not self.window.menu_opened:
            self.player.stop_movement()
            self.keys_pressed.clear()
            self.window.switch_view_to_menu_view()

        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_buttons_pressed[button] = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button in self.mouse_buttons_pressed:
            del self.mouse_buttons_pressed[button]


class TutorialGameView(GameView):
    def __init__(self, window, level_path: str = LevelPaths.test_level_2):
        super().__init__(window, level_path)

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        self.ground_list.draw()
        self.wall_list.draw()
        self.finish_list.draw()
        self.decoration_list.draw()
        self.decoration_list_2.draw()

        self.draw_text_()

        self.health_bottle_list.draw()
        self.medals_list.draw()
        self.spikes_list.draw()
        self.enemies_list.draw()

        self.player_list.draw()
        self.additional_sprites.draw()
        self.projectile_list.draw()
        self.secret_walls_list.draw()

        self.gui_camera.use()
        self.hud.display_health(self.player.current_health)
        self.hud.display_mana(self.player.current_mana)
        self.hud.display_currency(self.medals)

    def draw_text_(self):
        batch = Batch()

        text_color = (166, 104, 67)

        text_1 = arcade.Text(
            "Нажимайте WASD,",
            215, 260,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_2 = arcade.Text(
            "чтобы передвигаться.",
            215, 230,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_3 = arcade.Text(
            "Не наступайте",
            215, 800,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_4 = arcade.Text(
            "на шипы!",
            215, 770,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_5 = arcade.Text(
            "Нажмите пробел,",
            215, 1340,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_6 = arcade.Text(
            "чтобы сделать рывок.",
            215, 1310,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_7 = arcade.Text(
            "Во время рывка",
            215, 1280,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_9 = arcade.Text(
            "вы неуязвимы.",
            215, 1250,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_10 = arcade.Text(
            "Впереди враг!",
            215, 1860,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_11 = arcade.Text(
            "Нажимайте ЛКМ,",
            215, 1830,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_12 = arcade.Text(
            "чтобы делать удары.",
            215, 1800,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_13 = arcade.Text(
            "Нажимайте ПКМ,",
            215, 1770,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_14 = arcade.Text(
            "чтобы использовать магию.",
            215, 1740,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_15 = arcade.Text(
            "Это медальки,",
            215, 2890,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_16 = arcade.Text(
            "они используются",
            215, 2860,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_17 = arcade.Text(
            "для покупок в магазине.",
            215, 2830,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_18 = arcade.Text(
            "Пройдите в выход",
            215, 3400,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        text_19 = arcade.Text(
            "для завершения уровня.",
            215, 3370,
            color=text_color,
            font_size=20,
            font_name='Kenney Pixel',
            batch=batch)

        batch.draw()

