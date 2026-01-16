import arcade
from src.entities.enemies import BaseEnemy
from src.constants import WARRIOR_DAMAGE, WARRIOR_SPEED, WARRIOR_MAX_HEALTH


class Warrior(BaseEnemy):
    def __init__(self, max_health: float = WARRIOR_MAX_HEALTH, damage: float = WARRIOR_DAMAGE,
                 speed: float = WARRIOR_SPEED):
        super().__init__(
            invincibility_time=0,
            max_health=max_health,
            damage=damage,
            speed=speed
        )


