from dataclasses import dataclass
from _bootstrap import PROJECT_ROOT


@dataclass
class TexturePaths:
    """Датакласс для хранения путей к текстурам"""

    default_entity = ":resources:/images/animated_characters/male_person/malePerson_idle.png"

    player = str(PROJECT_ROOT / "resources/textures/entities/player/player.png")
    player_walk_1 = str(PROJECT_ROOT / "resources/textures/entities/player/walk_1.png")
    player_walk_2 = str(PROJECT_ROOT / "resources/textures/entities/player/walk_2.png")
    player_walk_3 = str(PROJECT_ROOT / "resources/textures/entities/player/walk_3.png")
    player_walk_4 = str(PROJECT_ROOT / "resources/textures/entities/player/walk_4.png")

    sword_1 = str(PROJECT_ROOT / "resources/textures/sword_1.png")
    sword_2 = str(PROJECT_ROOT / "resources/textures/sword_2.png")
    axe_1 = str(PROJECT_ROOT / "resources/textures/axe_1.png")
    axe_2 = str(PROJECT_ROOT / "resources/textures/axe_2.png")
    bow = str(PROJECT_ROOT / "resources/textures/bow.png")
    arrow = str(PROJECT_ROOT / "resources/textures/arrow.png")
    magic_ball = str(PROJECT_ROOT / "resources/textures/magic_ball.png")

    melee_attack_1 = str(PROJECT_ROOT / "resources/textures/melee_attack_1.png")
    melee_attack_2 = str(PROJECT_ROOT / "resources/textures/melee_attack_2.png")
    melee_attack_3 = str(PROJECT_ROOT / "resources/textures/melee_attack_3.png")
    melee_attack_4 = str(PROJECT_ROOT / "resources/textures/melee_attack_4.png")
    melee_attack_5 = str(PROJECT_ROOT / "resources/textures/melee_attack_5.png")

    transparent = str(PROJECT_ROOT / "resources/textures/transparent.png")

    warrior = str(PROJECT_ROOT / "resources/textures/entities/knight/knight.png")
    warrior_walk_1 = str(PROJECT_ROOT / "resources/textures/entities/knight/walk_1.png")
    warrior_walk_2 = str(PROJECT_ROOT / "resources/textures/entities/knight/walk_2.png")
    warrior_walk_3 = str(PROJECT_ROOT / "resources/textures/entities/knight/walk_3.png")
    warrior_walk_4 = str(PROJECT_ROOT / "resources/textures/entities/knight/walk_4.png")

    barbarian = str(PROJECT_ROOT / "resources/textures/entities/barbarian/barbarian.png")
    barbarian_walk_1 = str(PROJECT_ROOT / "resources/textures/entities/barbarian/walk_1.png")
    barbarian_walk_2 = str(PROJECT_ROOT / "resources/textures/entities/barbarian/walk_2.png")
    barbarian_walk_3 = str(PROJECT_ROOT / "resources/textures/entities/barbarian/walk_3.png")
    barbarian_walk_4 = str(PROJECT_ROOT / "resources/textures/entities/barbarian/walk_4.png")

    archer = str(PROJECT_ROOT / "resources/textures/entities/archer/archer.png")
    archer_walk_1 = str(PROJECT_ROOT / "resources/textures/entities/archer/walk_1.png")
    archer_walk_2 = str(PROJECT_ROOT / "resources/textures/entities/archer/walk_2.png")
    archer_walk_3 = str(PROJECT_ROOT / "resources/textures/entities/archer/walk_3.png")
    archer_walk_4 = str(PROJECT_ROOT / "resources/textures/entities/archer/walk_4.png")

    death_ghost_1 = str(PROJECT_ROOT / "resources/textures/death/death_ghost_1.png")
    death_ghost_2 = str(PROJECT_ROOT / "resources/textures/death/death_ghost_2.png")
    death_ghost_3 = str(PROJECT_ROOT / "resources/textures/death/death_ghost_3.png")
    death_ghost_4 = str(PROJECT_ROOT / "resources/textures/death/death_ghost_4.png")
    death_ghost_5 = str(PROJECT_ROOT / "resources/textures/death/death_ghost_5.png")

    ui_full_heart = str(PROJECT_ROOT / "resources/textures/ui/full_heart.png")
    ui_half_heart = str(PROJECT_ROOT / "resources/textures/ui/half_heart.png")
    ui_empty_heart = str(PROJECT_ROOT / "resources/textures/ui/empty_heart.png")

    ui_full_mana_ball = str(PROJECT_ROOT / "resources/textures/ui/full_mana_ball.png")
    ui_empty_mana_ball = str(PROJECT_ROOT / "resources/textures/ui/empty_mana_ball.png")

    ui_medal = str(PROJECT_ROOT / "resources/textures/ui/medal.png")


@dataclass
class SoundPaths:
    """Датакласс для хранения путей к звукам"""
    
    player_shot = str(PROJECT_ROOT / "resources/sounds/player/shot.wav")
    player_pain = str(PROJECT_ROOT / "resources/sounds/player/pain.wav")
    player_died = str(PROJECT_ROOT / "resources/sounds/player/died.wav")
    player_sword = str(PROJECT_ROOT / "resources/sounds/player/sword.wav")
    player_slesh = str(PROJECT_ROOT / "resources/sounds/player/slesh.wav")
    player_steps_v1 = str(PROJECT_ROOT / "resources/sounds/player/steps_v1.wav")
    player_steps_v2 = str(PROJECT_ROOT / "resources/sounds/player/steps_v2.wav")
    
    enemy_died = str(PROJECT_ROOT / "resources/sounds/enemies/died_enemy.wav")
    enemy_hit = str(PROJECT_ROOT / "resources/sounds/enemies/hit.wav")


@dataclass
class LevelPaths:
    """Датакласс для хранения путей к уровням"""

    test_level = str(PROJECT_ROOT / "resources/levels/test_map_3.tmx")
    test_level_2 = str(PROJECT_ROOT / "resources/levels/test_map_2.tmx")

    level_0 = str(PROJECT_ROOT / "resources/levels/level_0.tmx")
    level_1 = str(PROJECT_ROOT / "resources/levels/level_1.tmx")
    level_2 = str(PROJECT_ROOT / "resources/levels/level_2.tmx")
    level_3 = str(PROJECT_ROOT / "resources/levels/level_3.tmx")
