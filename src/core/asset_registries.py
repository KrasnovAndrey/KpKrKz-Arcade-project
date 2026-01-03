from dataclasses import dataclass
from src.core.paths import root


@dataclass
class TexturePaths:
    """Датакласс для хранения путей к текстурам"""

    default_entity = ":resources:/images/animated_characters/male_person/malePerson_idle.png"
    player = str(root / "resources/textures/entities/player.png")
