import arcade
from src.core.asset_registries import LevelPaths
from src.constants import TILE_SCALING, BACKGROUND_COLOR, CAMERA_LERP
from src.entities import Player
from src.entities.enemies import Warrior, Barbarian, Archer


class GameView(arcade.View):
    def __init__(self, window, level_path: str = LevelPaths.test_level_2):
        super().__init__(window)
        self.level_path = level_path

        self.keys_pressed = set()
        self.mouse_buttons_pressed = dict()

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

        self.physics_engines = []

        self.projectile_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.additional_sprites = arcade.SpriteList()

        self.spawn_enemies()
        self.player = None
        self.spawn_player()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

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

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        self.ground_list.draw()
        self.wall_list.draw()
        self.finish_list.draw()
        self.decoration_list.draw()
        self.spikes_list.draw()
        self.enemies_list.draw()
        self.player_list.draw()
        self.additional_sprites.draw()
        self.projectile_list.draw()

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

        self.additional_sprites.extend(self.player.setup_additional_sprites())

        physics_engine = arcade.PhysicsEngineSimple(self.player, self.collision_list)
        self.physics_engines.append(physics_engine)

    def spawn_medals(self):
        # TODO: Сделать спавн медалек
        pass

    def update_enemies_detection(self, delta_time: float):
        for enemy in self.enemies_list:
            enemy.update_detection(delta_time)

    def update_physics(self):
        for physics_engine in self.physics_engines:
            physics_engine.update()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_buttons_pressed[button] = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button in self.mouse_buttons_pressed:
            del self.mouse_buttons_pressed[button]
