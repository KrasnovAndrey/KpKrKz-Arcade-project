import os
import sqlite3
from pathlib import Path


APP_NAME = "KpKrKz-Arcade-project"
DB_NAME = "save.db"


def get_save_directory() -> Path:
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        if appdata:
            base_dir = Path(appdata)
        else:
            base_dir = Path.home() / "AppData" / "Roaming"
        return base_dir / APP_NAME
    home = Path.home()
    return home / ".local" / "share" / APP_NAME


def get_save_db_path() -> Path:
    save_dir = get_save_directory()
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir / DB_NAME


def init_db() -> None:
    db_path = get_save_db_path()
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS game_data (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                level INTEGER NOT NULL,
                medals INTEGER NOT NULL,
                melee_damage_modifier REAL NOT NULL,
                range_damage_modifier REAL NOT NULL,
                speed_modifier REAL NOT NULL
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def load_game_data() -> dict | None:
    db_path = get_save_db_path()
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level, medals, melee_damage_modifier, range_damage_modifier, speed_modifier FROM game_data WHERE id = 1"
        )
        row = cursor.fetchone()
        if row is None:
            return None
        level, medals, melee_damage_modifier, range_damage_modifier, speed_modifier = row
        return {
            "level": level,
            "medals": medals,
            "melee_damage_modifier": melee_damage_modifier,
            "range_damage_modifier": range_damage_modifier,
            "speed_modifier": speed_modifier,
        }
    finally:
        connection.close()


def save_game_data(data: dict) -> None:
    db_path = get_save_db_path()
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO game_data (id, level, medals, melee_damage_modifier, range_damage_modifier, speed_modifier)
            VALUES (1, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                level = excluded.level,
                medals = excluded.medals,
                melee_damage_modifier = excluded.melee_damage_modifier,
                range_damage_modifier = excluded.range_damage_modifier,
                speed_modifier = excluded.speed_modifier
            """,
            (
                data["level"],
                data["medals"],
                data["melee_damage_modifier"],
                data["range_damage_modifier"],
                data["speed_modifier"],
            ),
        )
        connection.commit()
    finally:
        connection.close()
