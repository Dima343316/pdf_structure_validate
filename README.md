***Описание проекта***

# Название: PDF Structure Validator

Этот проект предназначен для извлечения текста и штрихкодов из PDF-файлов и проверки других PDF-документов на соответствие эталонной структуре. Используется для автоматической валидации PDF-документов на наличие текста и штрихкодов в нужных местах.
Основные функции:

    Извлечение данных из PDF:
    Преобразует PDF в изображения, извлекает текст с помощью OCR (pytesseract) и данные штрихкодов (pyzbar).

    Проверка соответствия с эталоном:
    Сравнивает текст и штрихкоды тестируемого PDF с эталонным, выводя отчёт о различиях.

Технологии:

    pdf2image: конвертация PDF в изображения.
    pytesseract: OCR для извлечения текста.
    pyzbar: извлечение штрихкодов.
    pytest: для тестирования.

***Установка:***

Через докер командой - docker-compose build


***Что делает проект:***

    Основная цель: Этот проект предназначен для сравнения PDF файлов. Он берет один эталонный PDF и проверяет другие PDF файлы (тестовые) на соответствие эталону.
    Как работает:
        Процесс начинается с преобразования каждого PDF в изображения.
        Для каждого изображения извлекается текст с помощью OCR (Tesseract).
        Также извлекаются штрихкоды с использованием библиотеки pyzbar.
        Затем происходит сравнение текста и штрихкодов из эталонного и тестового файла.
    Результат: Программа генерирует отчет о различиях между эталонным и тестовым файлом. В отчете будет указано:
        Различия в тексте на страницах (например, если на одной странице текст отличается).
        Различия в количестве или содержимом штрихкодов.

***ПРИМЕР ВЫВОДА ДОКЕР КОНТЕЙНЕРА НА ТЕСТОВЫХ ФАЙЛАХ:***
pdf_validator-pdf_validator-1  | test_pdf_validate.py::test_pdf_structure 
pdf_validator-pdf_validator-1  | Найдено 2 штрихкодов на изображении.
pdf_validator-pdf_validator-1  | Тип: CODE128, Данные: 1
pdf_validator-pdf_validator-1  | Тип: CODE128, Данные: tst
pdf_validator-pdf_validator-1  | Найдено 2 штрихкодов на изображении.
pdf_validator-pdf_validator-1  | Тип: CODE128, Данные: 1
pdf_validator-pdf_validator-1  | Тип: CODE128, Данные: tst
pdf_validator-pdf_validator-1  | Текст совпадает на всех страницах.
pdf_validator-pdf_validator-1  | Штрихкоды совпадают на всех страницах.
pdf_validator-pdf_validator-1  | PDF соответствует эталону.
pdf_validator-pdf_validator-1  | PASSED
pdf_validator-pdf_validator-1  | 
pdf_validator-pdf_validator-1  | 
pdf_validator-pdf_validator-1  | ============================== 1 passed in 0.83s ===============================


***УСТАНОВКА ЧЕРЕЗ КОНСОЛЬ ПРОЕКТА:***
Перед тем как запустить проект, необходимо установить все зависимости:

pip install -r requirements.txt

Кроме того, для работы с OCR (распознавание текста на изображениях) требуется установить Tesseract и настроить переменную окружения.
Установка Tesseract

    Для Linux (Ubuntu/Debian):

    sudo apt-get install tesseract-ocr

    Для macOS (через Homebrew):

    brew install tesseract

    Для Windows: Скачайте и установите Tesseract с официального сайта. Убедитесь, что путь к установке добавлен в переменную окружения PATH.

***Пример использования***

from pdf_structure_validator import PdfStructureValidator

# Создаем валидатор с путем к эталонному PDF
validator = PdfStructureValidator(reference_pdf_path="path_to_reference_pdf")

# Валидируем тестовый PDF
report = validator.validate_pdf(test_pdf_path="path_to_test_pdf")

# Выводим отчет о различиях
for line in report:
    print(line)

или можете запустить тесты командой - pytest -sv
