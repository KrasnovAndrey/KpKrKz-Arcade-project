import arcade
from src.entities.projectiles import MeleeAttack


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

        self.player = player
        self.mana_per_hit = mana_per_hit
        self.mana_gifted = False

    def update(self, delta_time):
        super().update(delta_time)

        if self.entities_hit_list and not self.mana_gifted:
            self.player.add_mana(self.mana_per_hit)
            self.mana_gifted = True

