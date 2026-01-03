"""
Добавляет корень проекта в sys.path.
Импортируйте этот файл ПЕРВЫМ в любом скрипте.
"""
import sys
from pathlib import Path


def add_project_to_path():
    """Находит корень проекта и добавляет его в sys.path."""

    # Варианты поиска корня
    possible_roots = []

    # 1. От места запуска скрипта
    if hasattr(sys, 'argv') and sys.argv[0]:
        script_path = Path(sys.argv[0]).resolve()
        # Поднимаемся пока не найдем src/
        for parent in script_path.parents:
            if (parent / "src").exists() and (parent / "config").exists():
                possible_roots.append(parent)

    # 2. От текущей рабочей директории
    cwd = Path.cwd()
    for parent in cwd.parents:
        if (parent / "src").exists() and (parent / "config").exists():
            possible_roots.append(parent)

    # 3. Проверяем саму cwd
    if (cwd / "src").exists() and (cwd / "config").exists():
        possible_roots.append(cwd)

    # Выбираем первый найденный
    if possible_roots:
        project_root = possible_roots[0]
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        return project_root

    # Если не нашли
    print("WARNING: Could not find project root. Using current directory.")
    sys.path.insert(0, str(cwd))
    return cwd


PROJECT_ROOT = add_project_to_path()