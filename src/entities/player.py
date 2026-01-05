import arcade
from .base_entity import BaseEntity
from src.constants import PLAYER_MAX_HEALTH, PLAYER_SPEED, PLAYER_INVINCIBILITY_TIME, PLAYER_MAX_MANA, \
    PLAYER_MELEE_DAMAGE, PLAYER_RANGE_DAMAGE, PLAYER_RANGE_MANA_COST, PLAYER_ATTACK_COOLDOWN_TIME, \
    PLAYER_DASH_SPEED_MULTIPLIER, PLAYER_DASH_DURATION, PLAYER_DASH_COOLDOWN, PLAYER_NORMAL_ALPHA, PLAYER_FLASH_ALPHA


class Player(BaseEntity):
    """Класс игрока"""

    def __init__(
            self,
            max_health: float = PLAYER_MAX_HEALTH,
            speed: float = PLAYER_SPEED,
            scale: float = 1.0,
            texture_path: str = None,
            invincibility_time: float = PLAYER_INVINCIBILITY_TIME,
            normal_alpha: int = PLAYER_NORMAL_ALPHA,
            flash_alpha: int = PLAYER_FLASH_ALPHA,
            max_mana: float = PLAYER_MAX_MANA,
            melee_damage: float = PLAYER_MELEE_DAMAGE,
            range_damage: float = PLAYER_RANGE_DAMAGE,
            range_mana_cost: float = PLAYER_RANGE_MANA_COST,
            dash_speed_multiplier: float = PLAYER_DASH_SPEED_MULTIPLIER,
            dash_duration: float = PLAYER_DASH_DURATION,
            dash_cooldown: float = PLAYER_DASH_COOLDOWN,
            attack_cooldown_time: float = PLAYER_ATTACK_COOLDOWN_TIME

    ):
        super().__init__(
            max_health=max_health,
            damage=melee_damage,
            speed=speed,
            scale=scale,
            texture_path=texture_path,
            invincibility_time=invincibility_time,
            normal_alpha=normal_alpha,
            flash_alpha=flash_alpha,
        )

        self.original_speed = speed

        # Мана
        self.max_mana = max_mana
        self.current_mana = max_mana

        # Атаки
        self.melee_damage = melee_damage
        self.range_damage = range_damage
        self.range_mana_cost = range_mana_cost

        # Состояния атак
        self.is_attacking = False
        self.attack_cooldown = 0.0
        self.attack_cooldown_time = attack_cooldown_time

        # Рывок
        # TODO: Заменить числа константами из constants.py
        self.dash_speed_multiplier = dash_speed_multiplier  # Во сколько раз ускоряется
        self.dash_duration = dash_duration  # Длительность рывка в секундах
        self.dash_cooldown = dash_cooldown # Кулдаун в секундах
        self.dash_timer = 0.0
        self.dash_cooldown_timer = 0.0
        self.is_dashing = False
        self.dash_invincibility = True  # Включать ли неуязвимость
        self.dash_direction_x = None
        self.dash_direction_y = None

        self.input_locked = False

        self.name = "Player"

    def update(self, delta_time: float):
        super().update(delta_time)

        # Кулдаун атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown = max(0, self.attack_cooldown - delta_time)

        # Таймер рывка
        if self.is_dashing:
            self.dash_timer -= delta_time
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.input_locked = False
                self.speed = self.original_speed

        # Таймер кулдауна рывка
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= delta_time

    def move_with_keys(self, keys: set):
        """
        Управление по клавишам.
        """

        self.change_x = 0.0
        self.change_y = 0.0

        # Обрабатываем нажатия
        if arcade.key.W in keys or arcade.key.UP in keys:
            self.change_y = 1.0
        if arcade.key.S in keys or arcade.key.DOWN in keys:
            self.change_y = -1.0
        if arcade.key.A in keys or arcade.key.LEFT in keys:
            self.change_x = -1.0
        if arcade.key.D in keys or arcade.key.RIGHT in keys:
            self.change_x = 1.0
        if arcade.key.SPACE in keys:
            self.dash()

        # Нормализуем диагональное движение
        if self.change_x != 0 and self.change_y != 0:
            self.change_x *= 0.7071
            self.change_y *= 0.7071

    def melee_attack(self):
        """
        Ближняя атака.
        """
        if self.attack_cooldown > 0 or not self.is_alive:
            return False

        self.is_attacking = True
        self.attack_cooldown = self.attack_cooldown_time

        return True

    def range_attack(self):
        """
        Дальняя атака
        """
        if self.attack_cooldown > 0 or not self.is_alive:
            return False

        if self.current_mana < self.range_mana_cost:
            return False

        self.current_mana -= self.range_mana_cost

        self.is_attacking = True
        self.attack_cooldown = self.attack_cooldown_time

        # TODO: Создание снаряда
        # TODO: Анимация и звук

        return True

    def get_mana(self) -> float:
        """Получить текущую ману"""
        return self.current_mana

    def get_mana_percentage(self) -> float:
        """Получить процент маны (0.0 - 1.0)."""
        return self.current_mana / self.max_mana if self.max_mana > 0 else 0.0

    def add_mana(self, amount: float):
        """Добавить ману."""
        self.current_mana = min(self.max_mana, self.current_mana + amount)

    def use_mana(self, amount: float) -> bool:
        """
        Попытаться использовать ману.
        Возвращает True если успешно, False если не хватило.
        """
        if self.current_mana >= amount:
            self.current_mana -= amount
            return True
        return False

    def can_use_range_attack(self) -> bool:
        """Можно ли использовать дальнюю атаку."""
        return (
                self.is_alive and
                self.attack_cooldown <= 0 and
                self.current_mana >= self.range_mana_cost
        )

    def can_use_melee_attack(self) -> bool:
        """Можно ли использовать ближнюю атаку."""
        return self.is_alive and self.attack_cooldown <= 0

    def can_dash(self) -> bool:
        """
        Проверяет можно ли использовать рывок.
        """
        return (
                (self.change_x != 0 or self.change_y != 0) and # Есть направление, куда делать рывок
                self.is_alive and
                not self.is_dashing and  # Не во время рывка
                self.dash_cooldown_timer <= 0 and
                (self.change_x != 0 or self.change_y != 0)  # Есть движение
        )

    def dash(self):
        """
        Рывок в направлении текущего движения.
        Возвращает True если рывок успешно выполнен.
        """
        # Проверяем можно ли использовать рывок
        if not self.can_dash():
            return False

        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cooldown_timer = self.dash_cooldown

        self.dash_direction_x = self.change_x
        self.dash_direction_y = self.change_y

        # Нормализуем направление рывка
        length = (self.dash_direction_x ** 2 + self.dash_direction_y ** 2) ** 0.5
        if length > 0:
            self.dash_direction_x /= length
            self.dash_direction_y /= length

        self.speed = self.speed * self.dash_speed_multiplier # Ускоряем персонажа для рывка


        self.input_locked = True

        # Включаем неуязвимость если нужно
        if self.dash_invincibility:
            self.set_invincible(self.dash_duration)

        return True

    def __str__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"HP: {self.current_health:.0f}/{self.max_health}, "
                f"MP: {self.current_mana:.0f}/{self.max_mana})")
