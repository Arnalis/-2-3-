import unittest
from main import is_valid_array


class TestIsValidArray(unittest.TestCase):
    """
    Тестирование функции is_valid_array графовым покрытием.
    Покрываются все вершины, рёбра, пары рёбер и основные пути.
    """

    def setUp(self):
        #Счётчики для отчёта
        self.covered_paths = []

    def check_result(self, description, input_data, expected, actual, path):
        """
        Печатает подробный отчёт по одному тесту и проверяет результат
        path — покрытый путь в графе
        """
        print(f"  Тест: {description}")
        print(f"    Входные данные: {input_data}")
        print(f"    Ожидаемый результат: {expected}")
        print(f"    Полученный результат: {actual}")
        print(f"    Покрытый путь: {path}")
        result = "ПРОЙДЕН" if actual == expected else "ПРОВАЛЕН"
        print(f"    Результат: {result}")
        print()
        self.covered_paths.append(path)
        self.assertEqual(actual, expected)

    #тест 1: покрывает путь [1, 2, 4, 6, 7] — означает, что оба условия - false
    def test_valid_array(self):
        self.check_result(
            "Валидный массив",
            "[1, 2, 3]",
            (True, ""),
            is_valid_array([1, 2, 3]),
            "[1, 2, 4, 6, 7]"
        )

    #тест 2: покрывает путь [1, 2, 3, 7] — означает, что первое условие - true
    def test_duplicates(self):
        self.check_result(
            "Массив с дубликатами",
            "[1, 2, 2]",
            (False, "Элементы массива должны быть различными"),
            is_valid_array([1, 2, 2]),
            "[1, 2, 3, 7]"
        )

    #тест 3: покрывает путь [1, 2, 4, 5, 7] — означает, что второе условие - true
    def test_out_of_range(self):
        self.check_result(
            "Число превышает предел 10^9",
            "[1, 10**10]",
            (False, "Элементы массива не должны превышать 10^9 по модулю"),
            is_valid_array([1, 10**10]),
            "[1, 2, 4, 5, 7]"
        )

    #тест 4: граница диапазона = |10^9|
    def test_negative_at_boundary(self):
        self.check_result(
            "Отрицательное число на границе",
            "[-10**9, 5]",
            (True, ""),
            is_valid_array([-10**9, 5]),
            "[1, 2, 4, 6, 7]"
        )

    #тест 5: ровно на верхней границе
    def test_exactly_max_value(self):
        self.check_result(
            "Значение ровно 10^9",
            "[10**9]",
            (True, ""),
            is_valid_array([10**9]),
            "[1, 2, 4, 6, 7]"
        )

    #тест 6: массив из одного элемента
    def test_single_element(self):
        self.check_result(
            "Массив из одного элемента",
            "[42]",
            (True, ""),
            is_valid_array([42]),
            "[1, 2, 4, 6, 7]"
        )

    #тест 7: дубликаты с выходом за диапазон, где первое условие срабатывает раньше
    def test_duplicates_and_overflow(self):
        self.check_result(
            "Дубликаты и превышение одновременно",
            "[10**10, 10**10]",
            (False, "Элементы массива должны быть различными"),
            is_valid_array([10**10, 10**10]),
            "[1, 2, 3, 7]"
        )

    #тест 8: пустой массив — граничный случай
    def test_empty_array(self):
        self.check_result(
            "Пустой массив",
            "[]",
            (True, ""),
            is_valid_array([]),
            "[1, 2, 4, 6, 7]"
        )


if __name__ == "__main__":
    print("=" * 64)
    print("  ПРОГРАММА И МЕТОДИКА ИСПЫТАНИЙ")
    print("  Объект: функция is_valid_array из main.py (ЛР №1)")
    print("  Цель: проверка валидации массива по графовому покрытию")
    print("=" * 64)
    print()
    print("Граф функции:")
    print("  Вершины: {1, 2, 3, 4, 5, 6, 7}")
    print("  Рёбра:   {(1,2), (2,3), (2,4), (3,7), (4,5), (4,6), (5,7), (6,7)}")
    print("  Цикломатическая сложность: 8 - 7 + 2 = 3")
    print("  Основные пути:")
    print("    [1, 2, 3, 7]")
    print("    [1, 2, 4, 5, 7]")
    print("    [1, 2, 4, 6, 7]")
    print()
    print("=" * 64)
    print("  РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 64)
    print()

    unittest.main(verbosity=0)
