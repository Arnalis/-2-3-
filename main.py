import sys
# Сортировка пузырьком - возврат по возрастанию
def bubble_sort(array):

    if array is None:
        raise ValueError("Массив не может быть None")
    if not isinstance(array, list):
        raise TypeError("Ожидается список")

    length = len(array)
    swap_count = 0

    # Внешний цикл, за проход выводим максимум
    for current_index in range(length - 1):
        # Во внутреннем сравниваются соседние элементы
        for compare_index in range(length - current_index - 1):
            if array[compare_index] > array[compare_index + 1]:
                # свап, если левый > правый
                array[compare_index], array[compare_index + 1] = array[compare_index + 1], array[compare_index]
                swap_count += 1

    return array, swap_count

def parse_array_from_string(input_string, expected_length):
    """
    Преобразует строку с числами в СПИСОК целых чисел.
    Проверяет, что количество элементов соответствует ожидаемому.
    """
    tokens = input_string.split()
    if len(tokens) != expected_length:
        raise ValueError(f"Ожидалось {expected_length} элементов, получено {len(tokens)}")
    try:
        numbers = [int(token) for token in tokens]
    except ValueError:
        raise ValueError("Массив содержит нецелые числа")
    return numbers

def is_valid_array(array):
    """
    Проверяет дополнительные ограничения:
     1)все элементы различны;
     2) модуль каждого элемента не превышает 10^9.
    """
    if len(set(array)) != len(array):
        return False, "Элементы массива должны быть различными"
    if any(abs(element) > 10**9 for element in array):
        return False, "Элементы массива не должны превышать 10^9 по модулю"
    return True, ""

def main():
    """Ручной ввод с клавиатуры и вывод результата."""
    print("СОРТИРОВКА ПУЗЫРЬКОМ ")
    try:
        # Ввод количества элементов ( С КЛАВЫ )
        count_input = input("Введите количество элементов (n): ").strip()
        if not count_input:
            print("Ошибка: Пустая строка. Введите целое число.")
            return

        try:
            element_count = int(count_input)
        except ValueError:
            print("Ошибка: Количество элементов должно быть целым числом.")
            return

        if element_count < 1 or element_count > 1000:
            print(f"Ошибка: Количество элементов должно быть от 1 до 1000 (введено {element_count}).")
            return

        # Ввод массива (С КЛАВЫ )
        array_input = input(f"Введите {element_count} элементов массива через пробел: ").strip()
        if not array_input:
            print("Ошибка: Вы не ввели массив.")
            return

        try:
            array = parse_array_from_string(array_input, element_count)
        except ValueError as error:
            print(f"Ошибка: {error}")
            return

        # доп проверочки
        is_valid, error_message = is_valid_array(array)
        if not is_valid:
            print(f"Ошибка: {error_message}")
            return

        #  сама сортировка (вызов метода)
        sorted_array, swaps = bubble_sort(array)

        # Вывод результатов
        print("\n РЕЗУЛЬТАТ ")
        print("Отсортированный массив:", ' '.join(map(str, sorted_array)))
        print("Количество перестановок:", swaps)

    # Различные обработчики экшенов от юзеров
    except KeyboardInterrupt:
        print("\n\nДействие прервано пользователем.")
    except Exception as error:
        print(f"Произошла непредвиденная ошибка: {error}")

def run_tests_from_file(filename):
    """
    Автоматическое тестирование по файлу.
    Формат файла: для каждого теста три строки, смотрим на кол-во элментов, массив (через пробел), ожидаемое кол-во перестановок. Игноирируем empty space (strings)
    """
    # Через трай обрабатываем различные исключения и через ключевое слово except 
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            raw_lines = file.readlines()
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return
    except PermissionError:
        print(f"Ошибка: нет доступа к файлу '{filename}'.")
        return
    except Exception as error:
        print(f"Непредвиденная ошибка при чтении файла: {error}")
        return

    # Удаляем пустые строки и лишние пробелы
    lines = [line.strip() for line in raw_lines if line.strip()]

    # Файл должен содержать количество строк, кратное 3 
    if len(lines) % 3 != 0:
        print("Ошибка: количество непустых строк должно быть кратно 3.")
        return

    total_tests = len(lines) // 3
    passed_tests = 0

    #  Обработчик каждых трех строк как отдельное тестирование (итерация из 3 строк содержит 1 тест по логике описанной на строке 105)
    for block_index in range(total_tests):
        test_number = block_index + 1
        n_line = lines[block_index * 3]
        array_line = lines[block_index * 3 + 1]
        expected_line = lines[block_index * 3 + 2]

        # Проверяем количество элементов
        try:
            n = int(n_line)
        except ValueError:
            print(f"Тест {test_number}: ошибка в данных – n должно быть целым числом")
            continue

        if n < 1 or n > 1000:
            print(f"Тест {test_number}: ошибка в данных – n вне диапазона [1, 1000]")
            continue

        # Проверяем массив
        try:
            array = parse_array_from_string(array_line, n)
        except ValueError as error:
            print(f"Тест {test_number}: ошибка в данных – {error}")
            continue

        is_valid, error_message = is_valid_array(array)
        if not is_valid:
            print(f"Тест {test_number}: ошибка в данных – {error_message}")
            continue

        # Проверяем ожидаемое количество перестановок
        try:
            expected_swaps = int(expected_line)
        except ValueError:
            print(f"Тест {test_number}: ошибка – ожидаемое количество перестановок должно быть целым числом")
            continue

        # Запускаем сортировку и сравниваем результат
        _, actual_swaps = bubble_sort(array)
        if actual_swaps == expected_swaps:
            print(f"Тест {test_number}: да")
            passed_tests += 1
        else:
            print(f"Тест {test_number}: нет")

    print(f"Пройдено {passed_tests} из {total_tests} тестов")

if __name__ == "__main__":
    # Если программа запущена с аргументом 'test', выполняем автоматическое тестирование
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_tests_from_file("tests.txt")
    else:
        main()