import arcade
from typing import Tuple
from src.core.asset_registries import TexturePaths, SoundPaths


class BaseEntity(arcade.Sprite):
    """Базовый класс для всех живых существ в игре."""

    def __init__(
            self,
            max_health: float = 100.0,
            damage: float = 10.0,
            speed: float = 3.0,
            scale: float = 1.0,
            texture_path=None,
            invincibility_time: float = 3.0,
            normal_alpha: int = 255,
            flash_alpha: int = 64,
            change_face_direction: bool = True,
            play_animation: bool = False,
            animation_textures: list = None,
            animation_delay: float = 0.3,
            play_walk_animation: bool = False,
            walk_textures: list = None,
            walk_delay: float = 0.3,
            additional_sprites: tuple = tuple(),
            flip_additional_sprites_on_face_direction_change: bool = True
    ):

        if texture_path:
            super().__init__(texture_path, scale=scale)
        else:
            # Стандартная текстура, елси не указана другая
            super().__init__(TexturePaths.default_entity,
                             scale=scale)

        # Параметры сущности
        self.max_health = max_health
        self.current_health = max_health
        self.damage = damage
        self.speed = speed

        # Состояния
        self.is_alive = True

        self.is_invincible = False
        self.invincibility_time = invincibility_time  # Время неуязвимости после получения урона
        self.invincibility_timer = 0.0

        # Мигание сущности
        self.is_flashing = False
        self.flashing_timer = 0.0
        self.last_flash_time = 0.0

        # Движение
        self.change_x = 0.0
        self.change_y = 0.0

        # Направление взгляда: 1 - right, 0 - left
        self.face_direction = 1

        # Текстуры для анимаций
        self.stay_texture_right = self.texture
        self.stay_texture_left = self.texture.flip_horizontally()

        if animation_textures:
            self.animation_textures_right = [arcade.load_texture(file_path=file_path) for file_path in
                                             animation_textures]
            self.animation_textures_left = [texture.flip_horizontally() for texture in self.animation_textures_right]
            self.current_animation_textures = self.animation_textures_right
        else:
            self.animation_textures_right = []
            self.animation_textures_left = []
            self.current_animation_textures = []

        if walk_textures:
            self.walk_textures_right = [arcade.load_texture(file_path=file_path) for file_path in walk_textures]
            self.walk_textures_left = [texture.flip_horizontally() for texture in self.walk_textures_right]
            self.current_walk_textures = self.walk_textures_right
        else:
            self.walk_textures_right = []
            self.walk_textures_left = []
            self.current_walk_textures = []

        # Анимация/эффекты
        self.change_face_direction = change_face_direction

        self.play_animation = play_animation
        self.animation_delay = animation_delay
        self.animation_timer = self.animation_delay
        self.current_animation_texture_index = 0

        self.play_walk_animation = play_walk_animation
        self.walk_animation_delay = walk_delay
        self.walk_animation_timer = self.walk_animation_delay
        self.current_walk_animation_texture_index = 0

        self.original_color = self.color
        self.normal_alpha = normal_alpha
        self.flash_alpha = flash_alpha
        self.flashing_frequency = 0.35

        # Дополнительные спрайты, отрисовываются рядом с объектом
        self.additional_sprites = additional_sprites
        self.additional_sprite_list = arcade.SpriteList()
        self.additional_sprites_textures_right = []
        self.additional_sprites_textures_left = []
        self.flip_additional_sprites_on_face_direction_change = flip_additional_sprites_on_face_direction_change

    def take_damage(self, damage: float) -> bool:
        if self.is_invincible or not self.is_alive:
            return False

        self.current_health -= damage
        
        # Звук получения урона
        if hasattr(self, 'name') and self.name == "Player":
            arcade.play_sound(arcade.load_sound(SoundPaths.player_pain))
        else:
            arcade.play_sound(arcade.load_sound(SoundPaths.enemy_hit))

        self.set_invincible(self.invincibility_time)
        self.set_flashing(self.invincibility_time)

        if self.current_health <= 0:
            self.die()
            return True

        return False

    def die(self):
        self.is_alive = False
        self.current_health = 0
        
        # Звук смерти
        if hasattr(self, 'name') and self.name == "Player":
            arcade.play_sound(arcade.load_sound(SoundPaths.player_died))
        else:
            arcade.play_sound(arcade.load_sound(SoundPaths.enemy_died))

    def heal(self, amount: float):
        """Восстановление здоровья."""
        if not self.is_alive:
            return None

        self.current_health = min(self.max_health, self.current_health + amount)
        return None

    def set_invincible(self, duration: float):
        """Включить неуязвимость на время."""
        self.is_invincible = True
        self.invincibility_timer = duration

    def update(self, delta_time):
        """Обновление состояния каждую секунду."""
        super().update(delta_time)

        # Обновление таймеров
        if self.is_invincible:
            self.invincibility_timer -= delta_time
            if self.invincibility_timer <= 0:
                self.is_invincible = False

        if self.is_flashing:
            self.flashing_timer -= delta_time
            self._flash()
            if self.flashing_timer <= 0:
                self.is_flashing = False
                self.last_flash_time = 0
                self.alpha = self.normal_alpha

        # Обновление позиции
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

        # Обновляем направления взгляда при движении
        if self.change_face_direction:
            if self.change_x > 0 and self.face_direction == 0:
                self.set_face_direction_right()
            elif self.change_x < 0 and self.face_direction == 1:
                self.set_face_direction_left()

        # Анимации
        if not self.change_x and not self.change_y:
            # При прекращении движеня сбрасываем анимацию хотьбы
            self.current_walk_animation_texture_index = 0
            self.walk_animation_timer = self.walk_animation_delay
            if not self.play_animation:
                self.texture = self.stay_texture_right if self.face_direction == 1 else self.stay_texture_left

            # Проигрываем стандартную анимацию если персонаж не движется
            if self.play_animation and self.current_animation_textures:
                self.animation_timer += delta_time
                if self.animation_timer >= self.animation_delay:
                    self.animation_timer = 0
                    self.texture = self.current_animation_textures[self.current_animation_texture_index]
                    self.current_animation_texture_index += 1
                    if self.current_animation_texture_index == len(self.current_animation_textures):
                        self.current_animation_texture_index = 0
        else:
            # При начале движения сбрасываем стандартную анимацию
            self.current_animation_texture_index = 0
            self.animation_timer = self.animation_delay

            # Проигрываем анимацию хотьбы если персонаж движется
            if self.play_walk_animation and self.current_walk_textures:
                self.walk_animation_timer += delta_time
                if self.walk_animation_timer >= self.walk_animation_delay:

                    self.walk_animation_timer = 0
                    self.texture = self.current_walk_textures[self.current_walk_animation_texture_index]
                    self.current_walk_animation_texture_index += 1
                    if self.current_walk_animation_texture_index == len(self.current_walk_textures):
                        self.current_walk_animation_texture_index = 0

        # Обновляем дополнительные спрайты
        self.update_additional_sprites()

    def set_movement(self, direction: Tuple[float, float]):
        """Установить направление движения."""
        self.change_x, self.change_y = direction

    def set_speed(self, new_speed: float):
        self.speed = new_speed

    def change_movement(self, direction: Tuple[float, float]):
        """Изменить направление движения"""
        self.change_x += direction[0]
        self.change_y += direction[1]

    def stop_movement(self):
        """Остановить движение."""
        self.change_x = 0.0
        self.change_y = 0.0

    def get_health(self) -> float:
        """Получить здоровье"""
        return self.current_health

    def get_health_percentage(self) -> float:
        """Получить процент здоровья (0.0 - 1.0)."""
        return self.current_health / self.max_health if self.max_health > 0 else 0.0

    def set_flashing(self, duration: float):
        """Сделать мигающим на время"""
        self.is_flashing = True
        self.last_flash_time = duration
        self.flashing_timer = duration

    def _flash(self):
        """Мигание (может запускаться после получения урона)"""
        if self.last_flash_time - self.flashing_timer >= self.flashing_frequency:
            # Переключаем прозрачность
            if self.alpha == self.normal_alpha:
                self.alpha = self.flash_alpha
                if self.additional_sprite_list:
                    for sprite in self.additional_sprite_list:
                        sprite.alpha = self.flash_alpha
            else:
                self.alpha = self.normal_alpha
                if self.additional_sprite_list:
                    for sprite in self.additional_sprite_list:
                        sprite.alpha = self.normal_alpha

            self.last_flash_time = self.flashing_timer

    def set_face_direction_right(self):
        self.face_direction = 1
        self.texture = self.stay_texture_right
        self.current_animation_textures = self.animation_textures_right
        self.current_walk_textures = self.walk_textures_right

        for (sprite, x, y), new_texture in zip(self.additional_sprites, self.additional_sprites_textures_right):
            sprite.texture = new_texture

    def set_face_direction_left(self):
        self.face_direction = 0
        self.texture = self.stay_texture_left
        self.current_animation_textures = self.animation_textures_left
        self.current_walk_textures = self.walk_textures_left

        for (sprite, x, y), new_texture in zip(self.additional_sprites, self.additional_sprites_textures_left):
            sprite.texture = new_texture


    def setup_additional_sprites(self):
        """Добавляет все дополнительные спрайты в additional_sprite_list и возвращает его. Также сохраняет текстуры спрайтов"""
        if self.additional_sprites:
            for sprite, x, y in self.additional_sprites:
                self.additional_sprite_list.append(sprite)
                self.additional_sprites_textures_right.append(sprite.texture)
                self.additional_sprites_textures_left.append(sprite.texture.flip_horizontally())

        return self.additional_sprite_list

    def update_additional_sprites(self):
        """Обновляет позиции всех дополнительных спрайтов"""
        if self.additional_sprites:
            for sprite, x, y in self.additional_sprites:
                sprite.center_x = self.center_x + x
                sprite.center_y = self.center_y + y
                if self.flip_additional_sprites_on_face_direction_change and self.face_direction == 0:
                    sprite.center_x -= 2 * x

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(HP: {self.current_health}/{self.max_health})"
