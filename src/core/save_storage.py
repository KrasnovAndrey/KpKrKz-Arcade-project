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
