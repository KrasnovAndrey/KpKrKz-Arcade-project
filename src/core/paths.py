# path_utils.py
from pathlib import Path
import sys


def get_medaldungeon_root():
    """Возвращает путь к папке MedalDungeon"""
    # Если запущено из exe (pyinstaller)
    if getattr(sys, 'frozen', False):
        # Возвращаем папку, где лежит exe файл
        return Path(sys.executable).parent

    # Если запущено как скрипт Python
    if sys.argv and sys.argv[0]:  # Если запущен скрипт
        start = Path(sys.argv[0]).parent
    else:  # Если интерактивный режим
        start = Path.cwd()

    current = start.resolve()

    # Ищем папку с именем MedalDungeon
    while True:
        # Если текущая папка называется MedalDungeon - это она!
        if current.name == 'MedalDungeon':
            return current

        # Если дошли до корня файловой системы - останавливаемся
        if current == current.parent:
            break

        current = current.parent

    # Если не нашли - возвращаем стартовую папку
    return start


# Использование:
root = get_medaldungeon_root()
print(root) 