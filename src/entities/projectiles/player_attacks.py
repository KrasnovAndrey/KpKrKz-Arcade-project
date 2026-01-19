import arcade
from src.core.asset_registries import TexturePaths, SoundPaths
from src.entities.projectiles import BaseProjectile, MeleeAttack


class PlayerMeleeAttack(MeleeAttack):
    def __init__(
            self,
            player,
            x: float,
            y: float,
            angle: float = 0,
            damage: float = 20,
            scale: float = 1,
            hit_list: arcade.SpriteList = None,
            animation_delay: float = 0.025,
            mana_per_hit: float = 2,
    ):
        super().__init__(x=x, y=y, angle=angle, damage=damage, scale=scale, hit_list=hit_list,
                         animation_delay=animation_delay)

        # Звук удара мечом
        arcade.play_sound(arcade.load_sound(SoundPaths.player_sword))
        
        self.player = player
        self.mana_per_hit = mana_per_hit
        self.mana_gifted = False

    def update(self, delta_time):
        super().update(delta_time)

        if self.entities_hit_list and not self.mana_gifted:
            self.player.add_mana(self.mana_per_hit)
            self.mana_gifted = True


class PlayerRangeAttack(BaseProjectile):
    def __init__(
            self,
            x: float = 0,
            y: float = 0,
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
            texture_path=TexturePaths.magic_ball
        )

