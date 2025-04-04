Этот код представляет собой программу, которая реализует два классических метода шифрования: шифр Цезаря и шифр Виженера.

Основные функции программы
1. Работа с файлами
read_file(filename) - читает содержимое файла

write_file(filename, text) - записывает текст в файл

get_first_lines(text, n=5) - возвращает первые n строк текста

2. Шифр Цезаря
caesar_encrypt(text, key) - шифрует текст с заданным ключом (сдвигом)

caesar_decrypt(text, key) - дешифрует текст с заданным ключом

Особенности:

Работает с латинским и русским алфавитами (включая букву "Ё")

Сохраняет регистр букв

Не изменяет символы, не входящие в алфавиты

3. Шифр Виженера
vigenere_square(alphabet) - генерирует квадрат Виженера для заданного алфавита

vigenere_encrypt(text, key, alphabet) - шифрует текст с заданным ключом

vigenere_decrypt(text, key, alphabet) - дешифрует текст с заданным ключом

Особенности:

Работает только с кириллическим алфавитом

Поддерживает два варианта алфавита: стандартный и случайно перемешанный

Сохраняет регистр букв

Не изменяет символы, не входящие в алфавит

4. Интерфейс командной строки
caesar_cli() - интерфейс для работы с шифром Цезаря

vigenere_cli() - интерфейс для работы с шифром Виженера

main() - главное меню программы

Как работает программа
При запуске пользователь выбирает метод шифрования (Цезаря или Виженера) или выход.

В зависимости от выбора:

Для Цезаря: запрашивается числовой ключ, затем программа шифрует и дешифрует текст из файла "caesar_volume_test.txt"

Для Виженера: запрашивается текстовый ключ и тип алфавита, затем программа показывает квадрат Виженера и обрабатывает текст из файла "Vinzher_volume_test.txt"

Результаты сохраняются в файлы:

Для Цезаря: encC_Cesar.txt (зашифрованный), decC_Cesar.txt (расшифрованный)

Для Виженера: encV_Vishner.txt, decV_Vishner.txt

Программа также выводит первые 5 строк исходного, зашифрованного и расшифрованного текста.

Требования к файлам
Программа ожидает, что файлы с исходным текстом будут содержать не менее 2000 символов, иначе выдаст ошибку.

Программа поддерживает кириллические и латинские символы, сохраняет регистр и не изменяет символы, не входящие в алфавит (знаки препинания, цифры и т.д.).

