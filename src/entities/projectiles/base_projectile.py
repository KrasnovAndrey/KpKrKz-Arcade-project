import arcade
from src.entities import BaseEntity


class BaseProjectile(BaseEntity):
    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 damage: float = 3.0,
                 speed: float = 3.0,
                 scale: float = 1.0,
                 texture_path: str = None,
                 play_animation: bool = False,
                 animation_textures: list = None,
                 animation_delay: float = 0.3,
                 play_walk_animation: bool = False,
                 walk_textures: list = None,
                 walk_delay: float = 0.3,
                 direction: tuple = (0, 0),
                 hit_list: arcade.SpriteList = None,
                 obstacles_list: arcade.SpriteList = None,
                 despawn_on_collision: bool = False,
                 lifetime: float = 10.0,
                 die_on_time: bool = False
                 ):
        super().__init__(max_health=1,
                         damage=damage,
                         speed=speed,
                         scale=scale,
                         texture_path=texture_path,
                         invincibility_time=0,
                         change_face_direction=False,
                         play_animation=play_animation,
                         animation_textures=animation_textures,
                         animation_delay=animation_delay,
                         play_walk_animation=play_walk_animation,
                         walk_textures=walk_textures,
                         walk_delay=walk_delay)

        self.hit_list = hit_list
        self.obstacles_list = obstacles_list
        self.despawn_on_collision = despawn_on_collision
        self.lifetime = lifetime
        self.die_on_time = die_on_time

        self.center_x = x
        self.center_y = y
        self.set_movement(direction)
        self.beaten_list = arcade.SpriteList()

        self.entities_hit_list = None

    def update(self, delta_time):
        super().update(delta_time)

        
        if self.die_on_time:
            if self.lifetime > 0:
                self.lifetime -= delta_time
            else:
                self.die()

        # Столкновение с существом
        if self.hit_list:
            self.entities_hit_list = arcade.check_for_collision_with_list(self, self.hit_list)
            if self.entities_hit_list:
                for entity in self.entities_hit_list:
                    if entity not in self.beaten_list:
                        entity.take_damage(self.damage)
                        self.beaten_list.append(entity)
                if self.despawn_on_collision:
                    self.die()
        # Столкновение с препятствием (стеной)
        if self.obstacles_list:
            obstacles_hit_list = arcade.check_for_collision_with_list(self, self.obstacles_list)
            if obstacles_hit_list and self.despawn_on_collision:
                self.die()

    def die(self):
        super().die()
        self.remove_from_sprite_lists()


