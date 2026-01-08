from dataclasses import dataclass
from _bootstrap import PROJECT_ROOT


@dataclass
class TexturePaths:
    """Датакласс для хранения путей к текстурам"""

    default_entity = ":resources:/images/animated_characters/male_person/malePerson_idle.png"
    player = str(PROJECT_ROOT / "resources/textures/entities/player/player.png")
    player_walk_1 = str(PROJECT_ROOT/ "resources/textures/entities/player/walk_1.png")
    player_walk_2 = str(PROJECT_ROOT / "resources/textures/entities/player/walk_2.png")
    player_walk_3 = str(PROJECT_ROOT / "resources/textures/entities/player/walk_3.png")
    player_walk_4 = str(PROJECT_ROOT / "resources/textures/entities/player/walk_4.png")
    sword_1 = str(PROJECT_ROOT / "resources/textures/sword_1.png")


@dataclass
class LevelPaths:
    """Датакласс для хранения путей к уровням"""

    test_level = str(PROJECT_ROOT / "resources/levels/test_map.tmx")