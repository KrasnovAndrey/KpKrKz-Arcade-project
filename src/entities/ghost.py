import arcade
from src.core.asset_registries import TexturePaths


class Ghost(arcade.Sprite):
    """Класс призрака, который появляется при смерти существа"""

    def __init__(self, x: float, y: float, animation_delay: float = 0.075, lifetime: float = 10, speed: float = 500,
                 acceleration: float = 75,
                 animation_textures: tuple = (TexturePaths.death_ghost_1, TexturePaths.death_ghost_2,
                                              TexturePaths.death_ghost_3,
                                              TexturePaths.death_ghost_4, TexturePaths.death_ghost_5),
                 **kwargs):
        super().__init__(**kwargs)

        self.center_x = x
        self.center_y = y

        self.animation_delay = animation_delay
        self.lifetime = lifetime

        self.speed = speed
        self.acceleration = acceleration

        self.frame = 0
        self.textures = animation_textures
        self.animation_timer = self.animation_delay
        self.texture = arcade.load_texture(self.textures[self.frame])

        self.is_flying = False

    def update(self, delta_time: float):
        if self.lifetime > 0:
            self.lifetime -= delta_time
        else:
            self.despawn()

        if self.frame < len(self.textures) and self.animation_timer <= 0:
            self.animation_timer = self.animation_delay
            self.texture = arcade.load_texture(self.textures[self.frame])
            self.frame += 1
        else:
            self.animation_timer -= delta_time
            if self.frame == len(self.textures):
                self.fly_up()

        if self.is_flying:
            self.center_y += self.speed * delta_time
            self.speed += self.acceleration * delta_time

    def fly_up(self):
        self.is_flying = True

    def despawn(self):
        self.remove_from_sprite_lists()
