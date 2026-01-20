import arcade
from src.entities.projectiles import BaseProjectile
from src.core.asset_registries import TexturePaths
import math

class Arrow(BaseProjectile):
    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            angle: float = 0,
            damage: float = 3.0,
            speed: float = 3.0,
            scale: float = 1.0,
            direction: tuple = (0, 0),
            hit_list: arcade.SpriteList = None,
            obstacles_list: arcade.SpriteList = None
    ):
        super().__init__(
            x=x,
            y=y,
            damage=damage,
            speed=speed,
            scale=scale,
            direction=direction,
            hit_list=hit_list,
            obstacles_list=obstacles_list,
            despawn_on_collision=True,
            texture_path=TexturePaths.arrow
        )

        self.angle = angle

