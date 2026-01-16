"""
Добавляет корень проекта в sys.path.
Импортируйте этот файл ПЕРВЫМ в любом скрипте.
"""

import sys
import os
from pathlib import Path


def get_project_root() -> Path:
    # Случай 1: Запуск из pyinstaller (.exe)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Корень проекта - папка где лежит .exe файл
        exe_dir = Path(sys.executable).parent.absolute()
        return exe_dir

    # Случай 2: Запуск скрипта Python (обычный режим)
    try:
        # __file__ существует при обычном запуске
        bootstrap_path = Path(__file__).resolve()
        return bootstrap_path.parent.absolute()
    except NameError:
        # __file__ может не существовать в некоторых случаях
        pass

    # Случай 3: Запуск из интерактивной консоли или непонятно откуда
    return Path.cwd().absolute()


def setup_environment():
    """Настраивает окружение для работы."""

    root = get_project_root()

    # 1. Добавляем корень в Python path (только если не в pyinstaller)
    if not getattr(sys, 'frozen', False):
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))

    # 2. Меняем рабочую директорию на корень
    # (В pyinstaller не меняем, чтобы не сломать пути к ресурсам)
    if not getattr(sys, 'frozen', False):
        os.chdir(root)

    # 3. Для pyinstaller: добавляем путь к ресурсам если они в _MEIPASS
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        meipass = Path(sys._MEIPASS)
        if str(meipass) not in sys.path:
            sys.path.insert(0, str(meipass))

    return root


PROJECT_ROOT = setup_environment()
