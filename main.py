import re
import json
import argparse
import sys

# Словарь для хранения значений констант
constants = {}

def read_input_file(input_file):
    """Чтение входного файла."""
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден.")
        sys.exit(1)

def write_output_file(output_file, data):
    """Запись выходного текста в файл."""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка записи в файл {output_file}: {e}")
        sys.exit(1)

def check_syntax(input_text):
    """Проверка синтаксиса входного текста."""
    for line in input_text.splitlines():
        line = line.strip()

        # Пропуск комментариев
        if line.startswith("|#") and line.endswith("#|"):
            continue

        # Проверка синтаксиса массивов
        if match := re.match(r"\(\{(.*)\}\)", line):
            array_content = match.group(1).strip()
            elements = array_content.split(",")
            for element in elements:
                element = element.strip()
                if not re.match(r"^\d+(\.\d+)?$", element):
                    raise SyntaxError(f"Ошибка в массиве: неверное значение '{element}'")

        # Проверка синтаксиса имен
        elif re.match(r"^[a-z]+$", line):
            continue

        # Проверка чисел
        elif re.match(r"^\d+(\.\d+)?$", line):
            continue

        # Проверка объявления констант
        elif re.match(r"^[a-z]+ = .+$", line):
            continue

        # Проверка вычисления констант
        elif re.match(r"^\$\([a-z]+\)$", line):
            continue

        else:
            raise SyntaxError(f"Неизвестная конструкция: {line}")

    return True

def transform_to_json(input_text):
    """Трансформация входного текста в JSON."""
    output = {}
    for line in input_text.splitlines():
        line = line.strip()

        # Пропуск комментариев
        if line.startswith("|#") and line.endswith("#|"):
            continue

        # Массивы
        if match := re.match(r"\(\{(.*)\}\)", line):
            array_content = match.group(1).strip()
            elements = [el.strip() for el in array_content.split(",")]
            output["array"] = elements

        # Имена
        elif re.match(r"^[a-z]+$", line):
            output["name"] = line

        # Числа
        elif re.match(r"^\d+(\.\d+)?$", line):
            output["number"] = float(line) if '.' in line else int(line)

        # Объявление констант
        elif match := re.match(r"^([a-z]+) = (.+)$", line):
            name, value = match.groups()
            constants[name] = value
            output[name] = value

        # Вычисление констант
        elif match := re.match(r"^\$\(([a-z]+)\)$", line):
            name = match.group(1)
            if name in constants:
                output[name] = constants[name]
            else:
                raise ValueError(f"Константа '{name}' не определена")

    return output

def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Инструмент для работы с учебным конфигурационным языком")
    parser.add_argument("input_file", help="Путь к входному файлу")
    parser.add_argument("output_file", help="Путь к выходному файлу")
    args = parser.parse_args()

    try:
        input_text = read_input_file(args.input_file)
        check_syntax(input_text)
        output_data = transform_to_json(input_text)
        write_output_file(args.output_file, output_data)
        print(f"Преобразование завершено. Результат записан в {args.output_file}")
    except SyntaxError as e:
        print(f"Ошибка синтаксиса: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
