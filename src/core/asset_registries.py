from dataclasses import dataclass
from _bootstrap import PROJECT_ROOT


@dataclass
class TexturePaths:
    """Датакласс для хранения путей к текстурам"""

    default_entity = ":resources:/images/animated_characters/male_person/malePerson_idle.png"
    player = str(PROJECT_ROOT / "resources/textures/entities/player.png")
