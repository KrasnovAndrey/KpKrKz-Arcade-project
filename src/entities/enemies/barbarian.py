import arcade
from src.entities.enemies import BaseEnemy
from src.entities.projectiles import MeleeAttack, AxeProjectile
from src.entities import Ghost
from src.constants import BARBARIAN_SPEED, BARBARIAN_MAX_HEALTH, BARBARIAN_ATTACK_COOLDOWN, \
    BARBARIAN_MELEE_ATTACK_DISTANCE, BARBARIAN_WALK_ANIMATION_DELAY, BARBARIAN_LOCK_AFTER_TAKING_DAMAGE_TIME, \
    BARBARIAN_RANGE_DAMAGE, BARBARIAN_MELEE_DAMAGE, BARBARIAN_RANGE_SPEED, BARBARIAN_RANGE_ATTACK_DISTANCE
from src.core.asset_registries import TexturePaths
from math import sqrt
from src.utils.vector_utils import normalize_vector


class Barbarian(BaseEnemy):
    def __init__(
            self,
            max_health: float = BARBARIAN_MAX_HEALTH,
            melee_damage: float = BARBARIAN_MELEE_DAMAGE,
            range_damage: float = BARBARIAN_RANGE_DAMAGE,
            speed: float = BARBARIAN_SPEED,
            invincibility_time: float = 0,
            attack_cooldown: float = BARBARIAN_ATTACK_COOLDOWN,
            player_list: arcade.SpriteList = None,
            projectiles_list: arcade.SpriteList = None,
            collision_list: arcade.SpriteList = None
    ):

        # Доп. спрайт - меч в руке
        additional_sprite_1 = arcade.Sprite(TexturePaths.axe_2, scale=1)
        additional_sprite_2 = arcade.Sprite(TexturePaths.axe_2, scale=1)
        additional_sprite_3 = arcade.Sprite(TexturePaths.axe_1, scale=1)
        additional_sprite_1.texture = additional_sprite_1.texture.flip_horizontally()

        additional_sprites = ((additional_sprite_1, 21, 0),
                              (additional_sprite_2, -21, 0))

        walk_textures = (TexturePaths.barbarian_walk_1, TexturePaths.barbarian_walk_2, TexturePaths.barbarian_walk_3,
                         TexturePaths.barbarian_walk_4)

        super().__init__(
            invincibility_time=invincibility_time,
            max_health=max_health,
            damage=melee_damage,
            speed=speed,
            texture_path=TexturePaths.barbarian,
            additional_sprites=additional_sprites,
            play_walk_animation=True,
            walk_textures=walk_textures,
            walk_delay=BARBARIAN_WALK_ANIMATION_DELAY,
            collision_list=collision_list
        )

        self.melee_damage = melee_damage
        self.range_damage = range_damage

        self.attack_cooldown_time = attack_cooldown
        self.attack_cooldown = 0
        self.is_attacking = False

        self.projectiles_list = projectiles_list
        self.player_list = player_list

        self.locked = False
        self.lock_timer = 0

        self.sword_angle_change_time = 0

        self.axe_thrown = False

    def set_player_list(self, player_list: arcade.SpriteList):
        self.player_list = player_list

    def update(self, delta_time):
        if self.locked:
            self.lock_timer = max(0, self.lock_timer - delta_time)
            if self.lock_timer == 0:
                self.locked = False
                self.alpha = self.normal_alpha
                for sprite in self.additional_sprite_list:
                    sprite.alpha = self.normal_alpha

        else:
            super().update(delta_time)

            if self.player_detected and self.detected_player and self.is_alive:
                player_distance = sqrt(abs(self.center_x - self.detected_player.center_x) ** 2 + abs(
                    self.center_y - self.detected_player.center_y) ** 2)

                if player_distance < BARBARIAN_RANGE_ATTACK_DISTANCE and not self.axe_thrown:
                    self.range_attack(self.detected_player.center_x, self.detected_player.center_y)

                elif player_distance < BARBARIAN_MELEE_ATTACK_DISTANCE:
                    self.melee_attack(self.detected_player.center_x, self.detected_player.center_y)

                else:
                    direction = (self.detected_player.center_x - self.center_x,
                                 self.detected_player.center_y - self.center_y)

                    self.set_movement(normalize_vector(direction))

            if self.attack_cooldown > 0:
                self.attack_cooldown = max(self.attack_cooldown - delta_time, 0)

        if self.sword_angle_change_time > 0:
            self.sword_angle_change_time -= delta_time
        else:
            if self.sword_angle_change_time != 0:
                self.sword_angle_change_time = 0
            self.additional_sprite_list[0].angle = 0

    def melee_attack(self, x, y):
        """
        Ближняя атака.
        """

        if self.attack_cooldown > 0 or not self.is_alive:
            return False

        self.stop()

        self.is_attacking = True
        self.attack_cooldown = self.attack_cooldown_time

        x_diff = x - self.center_x
        y_diff = y - self.center_y
        attack_x = 0
        attack_y = 0
        attack_diff_x = 27
        attack_diff_y = 27

        angle = 0
        if abs(x_diff) >= abs(y_diff):
            if x_diff >= 0:
                angle = 0
                attack_x = self.center_x + attack_diff_x
                attack_y = self.center_y
                if self.face_direction == 0:
                    self.set_face_direction_right()
            else:
                angle = 180
                attack_x = self.center_x - attack_diff_x
                attack_y = self.center_y
                if self.face_direction == 1:
                    self.set_face_direction_left()
        else:
            if y_diff >= 0:
                angle = -90
                attack_x = self.center_x
                attack_y = self.center_y + attack_diff_y
            else:
                angle = 90
                attack_x = self.center_x
                attack_y = self.center_y - attack_diff_y

        attack = MeleeAttack(attack_x, attack_y, angle, scale=2.5, hit_list=self.player_list, damage=self.damage)

        if self.projectiles_list is not None:
            self.projectiles_list.append(attack)

        self.additional_sprite_list[0].angle = 40 if self.face_direction == 1 else -40
        self.sword_angle_change_time = attack.lifetime

        return True

    def range_attack(self, x, y):
        x_diff = x - self.center_x
        y_diff = y - self.center_y

        direction = normalize_vector((x_diff, y_diff))

        attack_x = self.center_x + direction[0] * 25
        attack_y = self.center_y + direction[1] * 25

        projectile = AxeProjectile(attack_x, attack_y, damage=self.range_damage, scale=1,
                                         speed=BARBARIAN_RANGE_SPEED, hit_list=self.player_list, direction=direction,
                                         obstacles_list=self.collision_list)

        if self.projectiles_list is not None:
            self.projectiles_list.append(projectile)

        self.additional_sprites[-1][0].remove_from_sprite_lists()
        self.additional_sprites = self.additional_sprites[:-1]
        self.axe_thrown = True

        self.lock(duration=BARBARIAN_LOCK_AFTER_TAKING_DAMAGE_TIME, change_alpha=False)

        return True

    def lock(self, duration: float, change_alpha: bool = True):
        self.locked = True
        self.lock_timer = duration
        self.stop()
        if change_alpha:
            self.alpha = self.flash_alpha
            for sprite in self.additional_sprite_list:
                sprite.alpha = self.flash_alpha

    def take_damage(self, damage: float) -> bool:
        self.lock(BARBARIAN_LOCK_AFTER_TAKING_DAMAGE_TIME)
        super().take_damage(damage)

    def die(self):
        super().die()
        self.stop()
        ghost = Ghost(self.center_x, self.center_y)
        self.projectiles_list.append(ghost)
        self.remove_from_sprite_lists()
        for sprite, x, y in self.additional_sprites:
            sprite.remove_from_sprite_lists()
