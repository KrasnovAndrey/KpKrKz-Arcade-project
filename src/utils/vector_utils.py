from math import sqrt


def normalize_vector(vector: tuple):
    """Возвращает вектор с тем же направлением и длиной в 1 в виде кортежа. Для нуль-вектора вернет (0, 0)"""
    x, y = vector
    length = sqrt(x ** 2 + y ** 2)

    return x / length if length != 0 else 0, y / length if length != 0 else 0

