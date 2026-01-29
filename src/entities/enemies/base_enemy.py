import arcade
from src.entities import BaseEntity
from math import sqrt


class BaseEnemy(BaseEntity):
    def __init__(self, detection_radius: float = 300.0, chasing_time: float = 2.0,
                 player_list: arcade.SpriteList = None, collision_list: arcade.SpriteList = None, **kwargs):
        super().__init__(**kwargs)

        # Зона обнаружения
        self.detection_radius = detection_radius
        self.player_detected = False
        self.detected_player = None
        self.detection_timer = 0.0
        self.chasing_time = chasing_time

        self.player_list = player_list

        self.collision_list = collision_list

        self.name = "Base Enemy"

    def update_detection(self, delta_time):
        """
        Обновляет обнаружение игрока в радиусе.
        """

        player_list = self.player_list
        if player_list is None:
            return None

        if self.detection_radius <= 0 or not self.is_alive:
            self.player_detected = False
            self.detected_player = None
            return None

        # Проверяем каждого игрока
        closest_player = None
        closest_distance = float('inf')

        for player in player_list:
            if not player.is_alive:
                continue

            distance = sqrt((self.center_x - player.center_x) ** 2 +
                            (self.center_y - player.center_y) ** 2)

            if distance < closest_distance:
                closest_distance = distance
                closest_player = player

        if closest_player and closest_distance <= self.detection_radius:
            self.player_detected = True
            self.detected_player = closest_player
            self.detection_timer = self.chasing_time

        else:
            # Таймер "забывания" про игрока
            if self.detection_timer > 0:
                self.detection_timer -= delta_time
            else:
                self.player_detected = False
                self.detected_player = None

        return None

    def die(self):
        super().die()
        self.stop()
