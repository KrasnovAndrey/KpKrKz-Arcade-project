from pathlib import Path
import sys


def get_project_root():
    """Возвращает путь к корню проекта"""

    # Если запущено из exe (pyinstaller)
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent

    # Определяем путь к текущему файлу (paths.py)
    current_file = Path(__file__).resolve()

    # paths.py -> core -> src -> MedalDungeon
    project_root = current_file.parent.parent.parent

    return project_root


# Использование:
root = get_project_root()
print(root) 