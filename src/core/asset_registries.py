from dataclasses import dataclass
from _bootstrap import PROJECT_ROOT


@dataclass
class TexturePaths:
    """Датакласс для хранения путей к текстурам"""

    default_entity = ":resources:/images/animated_characters/male_person/malePerson_idle.png"
    player = str(PROJECT_ROOT / "resources/textures/entities/player.png")


@dataclass
class LevelPaths:
    """Датакласс для хранения путей к уровням"""

    test_level = str(PROJECT_ROOT / "resources/levels/test_map.tmx")