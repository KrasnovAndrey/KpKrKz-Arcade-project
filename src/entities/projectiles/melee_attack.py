import arcade
from .base_projectile import BaseProjectile
from src.core.asset_registries import TexturePaths


class MeleeAttack(BaseProjectile):
    def __init__(self,
                 x: float,
                 y: float,
                 angle: float = 0,
                 damage: float = 20,
                 scale: float = 1,
                 hit_list: arcade.SpriteList = None,
                 animation_delay: float = 0.025,
                 ):
        animation_textures = (TexturePaths.melee_attack_1, TexturePaths.melee_attack_2, TexturePaths.melee_attack_3,
                              TexturePaths.melee_attack_4, TexturePaths.melee_attack_5)

        lifetime = animation_delay * (len(animation_textures) - 1)

        super().__init__(x=x,
                         y=y,
                         texture_path=TexturePaths.transparent,
                         damage=damage,
                         scale=scale,
                         hit_list=hit_list,
                         play_animation=True,
                         animation_textures=animation_textures,
                         animation_delay=animation_delay,
                         play_walk_animation=False,
                         die_on_time=True,
                         lifetime=lifetime
                         )

        hitbox_x = x
        hitbox_y = y

        if angle == 0:
            hitbox_x += 25
        elif angle == 180:
            hitbox_x -= 25
        elif angle == 90:
            hitbox_y -= 25
        elif angle == -90:
            hitbox_y += 25

        self.hit_box = arcade.hitbox.RotatableHitBox(points=[
            (-25, -60),  # Левый нижний
            (15, -40),  # Правый нижний
            (15, 40),  # Правый верхний
            (-25, 60)  # Левый верхний
        ],
        position=(hitbox_x, hitbox_y))
        self.angle = angle
