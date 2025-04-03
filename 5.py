import string
import time
import itertools
from datetime import timedelta
import json
import os
from typing import Dict, List, Optional, Union

# Константы
DICTIONARY_FILE = 'russian_dictionary.json'
DEFAULT_DICTIONARY_SIZE = 2000


# Функции для работы со словарем
def generate_russian_dictionary(size: int = DEFAULT_DICTIONARY_SIZE) -> List[str]:
    """Генерирует словарь русских слов заданного размера"""
    # В реальной программе следует использовать готовый словарь из файла
    # Здесь для примера генерируем "слова" из комбинаций букв
    from itertools import product

    russian_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    words = []

    # Генерируем слова разной длины
    word_length = 3
    while len(words) < size:
        for letters in product(russian_letters, repeat=word_length):
            word = ''.join(letters)
            words.append(word)
            if len(words) >= size:
                break
        word_length += 1

    return words[:size]


def save_dictionary(dictionary: List[str], filename: str = DICTIONARY_FILE) -> None:
    """Сохраняет словарь в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)


def load_dictionary(filename: str = DICTIONARY_FILE) -> List[str]:
    """Загружает словарь из файла"""
    if not os.path.exists(filename):
        dictionary = generate_russian_dictionary()
        save_dictionary(dictionary, filename)
        return dictionary

    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def translate_to_latin_layout(russian_word: str) -> str:
    """Переводит русское слово в латинскую раскладку"""
    layout = {
        'а': 'f', 'б': ',', 'в': 'd', 'г': 'u', 'д': 'l', 'е': 't',
        'ё': '`', 'ж': ';', 'з': 'p', 'и': 'b', 'й': 'q', 'к': 'r',
        'л': 'k', 'м': 'v', 'н': 'y', 'о': 'j', 'п': 'g', 'р': 'h',
        'с': 'c', 'т': 'n', 'у': 'e', 'ф': 'a', 'х': '[', 'ц': 'w',
        'ч': 'x', 'ш': 'i', 'щ': 'o', 'ъ': ']', 'ы': 's', 'ь': 'm',
        'э': "'", 'ю': '.', 'я': 'z'
    }
    return ''.join([layout.get(c, c) for c in russian_word.lower()])


def prepare_dictionary() -> List[str]:
    """Подготавливает словарь для использования в атаке"""
    russian_words = load_dictionary()
    return [translate_to_latin_layout(word) for word in russian_words]


# Функции анализа пароля
def get_alphabet_power(password: str) -> int:
    """Вычисляет мощность алфавита пароля"""
    power = 0
    if any(c.islower() for c in password):
        power += 26
    if any(c.isupper() for c in password):
        power += 26
    if any(c.isdigit() for c in password):
        power += 10
    if any(c in string.punctuation for c in password):
        power += len(string.punctuation)
    return power


def calculate_combinations(alphabet_power: int, length: int) -> int:
    """Вычисляет количество возможных комбинаций"""
    return alphabet_power ** length


def calculate_brute_force_time(
        combinations: int,
        speed: int = 1_000_000,
        attempts_before_pause: int = 1_000_000,
        pause_duration: int = 1
) -> timedelta:
    """Вычисляет время полного перебора"""
    total_attempts = combinations
    full_batches = total_attempts // attempts_before_pause
    remaining_attempts = total_attempts % attempts_before_pause

    total_pause_time = (full_batches - (1 if remaining_attempts == 0 else 0)) * pause_duration
    total_seconds = (total_attempts / speed) + total_pause_time

    return timedelta(seconds=total_seconds)


def analyze_password(
        password: str,
        speed: int = 1_000_000,
        attempts_before_pause: int = 1_000_000,
        pause_duration: int = 1
) -> Dict[str, Union[str, int, float, timedelta]]:
    """Анализирует стойкость пароля"""
    if not password:
        raise ValueError("Пароль не может быть пустым")

    alphabet_power = get_alphabet_power(password)
    combinations = calculate_combinations(alphabet_power, len(password))
    brute_force_time = calculate_brute_force_time(combinations, speed, attempts_before_pause, pause_duration)

    return {
        "password": password,
        "alphabet_power": alphabet_power,
        "combinations": combinations,
        "brute_force_time": brute_force_time,
        "password_length": len(password),
        "speed": speed,
        "attempts_before_pause": attempts_before_pause,
        "pause_duration": pause_duration
    }


# Функции для подбора пароля
def dictionary_attack(
        target_password: str,
        dictionary: List[str],
        max_attempts: Optional[int] = None
) -> Dict[str, Union[bool, str, int, float]]:
    """Атака по словарю"""
    start_time = time.time()
    attempts = 0

    for word in dictionary:
        attempts += 1
        if word == target_password:
            elapsed = time.time() - start_time
            return {
                "success": True,
                "password": target_password,
                "attempts": attempts,
                "time_seconds": elapsed,
                "speed": attempts / elapsed if elapsed > 0 else attempts,
                "method": "dictionary"
            }

        if max_attempts and attempts >= max_attempts:
            break

    elapsed = time.time() - start_time
    return {
        "success": False,
        "password": target_password,
        "attempts": attempts,
        "time_seconds": elapsed,
        "speed": attempts / elapsed if elapsed > 0 else attempts,
        "method": "dictionary"
    }


def brute_force_attack(
        target_password: str,
        max_length: Optional[int] = None,
        max_attempts: Optional[int] = None
) -> Dict[str, Union[bool, str, int, float]]:
    """Атака полным перебором"""
    if max_length is None:
        max_length = len(target_password)

    chars = []
    if any(c.islower() for c in target_password):
        chars.extend(string.ascii_lowercase)
    if any(c.isupper() for c in target_password):
        chars.extend(string.ascii_uppercase)
    if any(c.isdigit() for c in target_password):
        chars.extend(string.digits)
    if any(c in string.punctuation for c in target_password):
        chars.extend(string.punctuation)

    chars = list(set(chars))  # Удаляем дубликаты
    start_time = time.time()
    attempts = 0

    for length in range(1, max_length + 1):
        for guess in itertools.product(chars, repeat=length):
            attempts += 1
            guess_str = ''.join(guess)
            if guess_str == target_password:
                elapsed = time.time() - start_time
                return {
                    "success": True,
                    "password": target_password,
                    "attempts": attempts,
                    "time_seconds": elapsed,
                    "speed": attempts / elapsed if elapsed > 0 else attempts,
                    "method": "brute_force",
                    "max_length": max_length
                }

            if max_attempts and attempts >= max_attempts:
                elapsed = time.time() - start_time
                return {
                    "success": False,
                    "password": target_password,
                    "attempts": attempts,
                    "time_seconds": elapsed,
                    "speed": attempts / elapsed if elapsed > 0 else attempts,
                    "method": "brute_force",
                    "max_length": max_length
                }

    elapsed = time.time() - start_time
    return {
        "success": False,
        "password": target_password,
        "attempts": attempts,
        "time_seconds": elapsed,
        "speed": attempts / elapsed if elapsed > 0 else attempts,
        "method": "brute_force",
        "max_length": max_length
    }


# Основной класс программы
class PasswordSecurityAnalyzer:
    def __init__(self):
        self.dictionary = prepare_dictionary()

    def print_analysis(self, result: Dict) -> None:
        """Выводит результаты анализа"""
        print("\nРезультаты анализа пароля:")
        print(f"Пароль: {result['password']}")
        print(f"Длина пароля: {result['password_length']}")
        print(f"Мощность алфавита: {result['alphabet_power']}")
        print(f"Количество возможных комбинаций: {result['combinations']:.2e}")
        print(f"Предполагаемое время перебора: {result['brute_force_time']}")
        print(f"Скорость перебора: {result['speed']:,} паролей/секунду")
        print(f"Пауза после {result['attempts_before_pause']:,} попыток: {result['pause_duration']} сек")

    def print_attack_results(self, result: Dict) -> None:
        """Выводит результаты атаки"""
        if result['success']:
            print("\nПароль успешно подобран!")
            print(f"Метод: {result['method']}")
            print(f"Пароль: {result['password']}")
        else:
            print("\nПароль не удалось подобрать")
            print(f"Метод: {result['method']}")

        print(f"Попыток: {result['attempts']:,}")
        print(f"Затраченное время: {result['time_seconds']:.2f} секунд")
        print(f"Скорость перебора: {result['speed']:.2f} паролей/секунду")

        if 'max_length' in result:
            print(f"Максимальная длина перебора: {result['max_length']}")

    def run_password_analysis(self) -> None:
        """Режим анализа надежности пароля"""
        print("\nРежим анализа надежности пароля")
        password = input("Введите пароль для анализа: ")

        try:
            speed = int(input("Скорость перебора (паролей/сек) [1,000,000]: ") or 1_000_000)
            attempts = int(input("Количество попыток перед паузой [1,000,000]: ") or 1_000_000)
            pause = int(input("Длительность паузы (сек) [1]: ") or 1)

            result = analyze_password(password, speed, attempts, pause)
            self.print_analysis(result)

        except ValueError as e:
            print(f"Ошибка: {e}")

    def run_password_cracking(self) -> None:
        """Режим подбора пароля"""
        print("\nРежим подбора пароля для пользователя ADMIN")
        print("1. Подбор по словарю (русские слова в латинской раскладке)")
        print("2. Полный перебор всех возможных вариантов")

        choice = input("Выберите метод подбора (1/2): ")
        password = input("Введите пароль для подбора (имитация пароля ADMIN): ")

        if choice == '1':
            max_attempts = input("Максимальное количество попыток (Enter для без ограничений): ")
            max_attempts = int(max_attempts) if max_attempts else None

            print(f"\nИспользуется словарь из {len(self.dictionary):,} слов")
            result = dictionary_attack(password, self.dictionary, max_attempts)

        elif choice == '2':
            max_length = int(input("Максимальная длина пароля для перебора: "))
            max_attempts = input("Максимальное количество попыток (Enter для без ограничений): ")
            max_attempts = int(max_attempts) if max_attempts else None

            print("\nНачало полного перебора...")
            result = brute_force_attack(password, max_length, max_attempts)

        else:
            print("Неверный выбор метода")
            return

        self.print_attack_results(result)
        self.print_security_recommendations(result)

    def print_security_recommendations(self, attack_result: Dict) -> None:
        """Выводит рекомендации по безопасности на основе результатов"""
        print("\nРекомендации по безопасности паролей:")

        if attack_result['method'] == 'dictionary' and attack_result['success']:
            print("- Не используйте словарные слова, даже в другой раскладке")
            print("- Избегайте простых слов и общеупотребительных сочетаний")

        print("- Используйте пароли длиной не менее 12 символов")
        print("- Комбинируйте буквы (верхний и нижний регистр), цифры и спецсимволы")
        print("- Не используйте личную информацию (имена, даты рождения)")
        print("- Используйте мнемонические фразы вместо отдельных слов")
        print("- Регулярно меняйте важные пароли")

        print("\nСравнение методов атаки:")
        print("1. Подбор по словарю - эффективен против простых паролей")
        print("   Время подбора: от нескольких секунд до минут")
        print("2. Полный перебор - эффективен против сложных паролей")
        print("   Время подбора: от часов до миллионов лет для стойких паролей")

    def main_menu(self) -> None:
        """Главное меню программы"""
        while True:
            print("\nПрограмма анализа устойчивости парольной аутентификации")
            print("1. Проверка надежности пароля")
            print("2. Подбор пароля для пользователя ADMIN")
            print("3. Выход")

            choice = input("Выберите режим работы (1/2/3): ")

            if choice == '1':
                self.run_password_analysis()
            elif choice == '2':
                self.run_password_cracking()
            elif choice == '3':
                print("Завершение работы программы")
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")


# Запуск программы
if __name__ == "__main__":
    analyzer = PasswordSecurityAnalyzer()
    analyzer.main_menu()