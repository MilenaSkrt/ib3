import random
import os
from itertools import cycle


class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift
        self.alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    def encrypt(self, text):
        encrypted_text = []
        for char in text.upper():
            if char in self.alphabet:
                index = (self.alphabet.index(char) + self.shift) % len(self.alphabet)
                encrypted_text.append(self.alphabet[index])
            else:
                encrypted_text.append(char)
        return ''.join(encrypted_text)

    def decrypt(self, text):
        decrypted_text = []
        for char in text.upper():
            if char in self.alphabet:
                index = (self.alphabet.index(char) - self.shift) % len(self.alphabet)
                decrypted_text.append(self.alphabet[index])
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)


class VigenereCipher:
    def __init__(self, key, alphabet_type='ordered'):
        self.key = key.upper()
        self.alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        if alphabet_type == 'random':
            self.alphabet = ''.join(random.sample(self.alphabet, len(self.alphabet)))
        self.square = self.generate_vigenere_square()

    def generate_vigenere_square(self):
        square = []
        for i in range(len(self.alphabet)):
            shifted = self.alphabet[i:] + self.alphabet[:i]
            square.append(shifted)
        return square

    def print_square(self):
        print("Квадрат Виженера:")
        print("   " + " ".join(self.alphabet))
        for i, row in enumerate(self.square):
            print(f"{self.alphabet[i]} |" + " ".join(row))

    def encrypt(self, text):
        encrypted_text = []
        key_cycle = cycle(self.key)
        for char, key_char in zip(text.upper(), key_cycle):
            if char in self.alphabet:
                row = self.alphabet.index(key_char)
                col = self.alphabet.index(char)
                encrypted_text.append(self.square[row][col])
            else:
                encrypted_text.append(char)
        return ''.join(encrypted_text)

    def decrypt(self, text):
        decrypted_text = []
        key_cycle = cycle(self.key)
        for char, key_char in zip(text.upper(), key_cycle):
            if char in self.alphabet:
                row = self.alphabet.index(key_char)
                col = self.square[row].index(char)
                decrypted_text.append(self.alphabet[col])
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)


def process_file(input_filename, cipher, cipher_type):
    # Проверяем размер файла
    if os.path.getsize(input_filename) < 2000:
        print("Ошибка: файл должен содержать не менее 2000 символов")
        return

    # Чтение исходного файла
    with open(input_filename, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Создание имен выходных файлов
    base_name = os.path.splitext(input_filename)[0]
    enc_filename = f"enc{cipher_type}_{base_name}.txt"
    dec_filename = f"dec{cipher_type}_{base_name}.txt"

    # Шифрование и сохранение
    encrypted_text = cipher.encrypt(original_text)
    with open(enc_filename, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)

    # Дешифрование и сохранение
    decrypted_text = cipher.decrypt(encrypted_text)
    with open(dec_filename, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)

    # Вывод первых строк
    print("\nПервые строки файлов:")
    print(f"Исходный файл:\n{original_text[:500]}...")
    print(f"\nЗашифрованный файл:\n{encrypted_text[:500]}...")
    print(f"\nРасшифрованный файл:\n{decrypted_text[:500]}...")


def main():
    print("Программа криптографического преобразования текста")
    print("Выберите режим работы:")
    print("1. Шифр Цезаря")
    print("2. Шифр Виженера")

    choice = input("Ваш выбор (1 или 2): ")

    if choice == '1':
        # Режим Цезаря
        shift = int(input("Введите ключ (число) для шифра Цезаря: "))
        input_file = input("Введите имя файла для обработки (например, text.txt): ")

        cipher = CaesarCipher(shift)
        process_file(input_file, cipher, 'C')

    elif choice == '2':
        # Режим Виженера
        key = input("Введите ключ для шифра Виженера: ")
        alphabet_choice = input("Выберите тип алфавита (1 - по порядку, 2 - случайный): ")
        alphabet_type = 'ordered' if alphabet_choice == '1' else 'random'
        input_file = input("Введите имя файла для обработки (например, text.txt): ")

        cipher = VigenereCipher(key, alphabet_type)
        cipher.print_square()  # Выводим квадрат Виженера
        process_file(input_file, cipher, 'V')

    else:
        print("Неверный выбор. Завершение программы.")


if __name__ == "__main__":
    # Создаем тестовый файл, если его нет
    if not os.path.exists("test.txt"):
        sample_text = ("Криптография - это наука о методах обеспечения конфиденциальности "
                       "и аутентичности информации. " * 50)
        with open("test.txt", "w", encoding='utf-8') as f:
            f.write(sample_text)

    main()