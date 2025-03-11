import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from typing import List, Dict


class PdfStructureValidator:
    def __init__(self, reference_pdf_path: str, lang: str = 'eng'):
        self.reference_pdf_path = reference_pdf_path
        self.lang = lang

    def _convert_pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """Преобразование PDF в изображения."""
        try:
            images = convert_from_path(pdf_path)
            return images
        except Exception as e:
            raise Exception(f"Ошибка при конвертации PDF в изображения: {str(e)}")

    def _extract_text_from_image(self, image: Image.Image) -> Dict:
        """Извлечение текста с изображения с помощью Tesseract."""
        try:
            text_data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
            return text_data
        except Exception as e:
            raise Exception(f"Ошибка при извлечении текста с изображения: {str(e)}")

    def _extract_barcodes_from_image(self, image: Image.Image) -> List[Dict]:
        """Извлечение штрихкодов из изображения с помощью pyzbar."""
        barcodes = decode(image)
        barcode_data = [{'type': barcode.type, 'data': barcode.data.decode('utf-8')} for barcode in barcodes]

        if barcode_data:
            print(f"Найдено {len(barcodes)} штрихкодов на изображении.")
            for barcode in barcode_data:
                print(f"Тип: {barcode['type']}, Данные: {barcode['data']}")

        return barcode_data

    def _parse_text_data(self, text_data: Dict) -> List[Dict]:
        """Парсинг данных текста."""
        return [
            {
                'page_num': text_data['page_num'][i],
                'text': text_data['text'][i],
                'conf': text_data['conf'][i]
            }
            for i in range(len(text_data['text'])) if text_data['text'][i].strip()
        ]

    def _compare_text_data(self,
                           reference_data: List[Dict],
                           test_data: List[Dict]) -> List[Dict]:
        """Сравнение данных текста между двумя PDF."""
        differences = []

        for page_num, (ref_texts, test_texts) in enumerate(
                zip(reference_data, test_data), start=1):
            if len(ref_texts) != len(test_texts):
                differences.append({
                    'page_num': page_num,
                    'message': f"Различное количество текста на странице {page_num}: "
                               f"Эталонный: {len(ref_texts)} элементов, Тестовый: {len(test_texts)} элементов."
                })

            for ref_text, test_text in zip(ref_texts, test_texts):
                if ref_text['text'] != test_text['text']:
                    differences.append({
                        'page_num': page_num,
                        'ref_text': ref_text['text'],
                        'test_text': test_text['text']
                    })

        return differences

    def _compare_barcode_data(self, reference_data: List[Dict], test_data: List[Dict]) -> List[Dict]:
        """Сравнение данных штрихкодов между двумя PDF."""
        differences = []

        for page_num, (ref_barcodes, test_barcodes) in enumerate(zip(reference_data, test_data), start=1):
            if len(ref_barcodes) != len(test_barcodes):
                differences.append({
                    'page_num': page_num,
                    'message': f"Различное количество штрихкодов на странице {page_num}: "
                               f"Эталонный: {len(ref_barcodes)} штрихкодов, Тестовый: {len(test_barcodes)} штрихкодов."
                })

            for ref_barcode, test_barcode in zip(ref_barcodes, test_barcodes):
                if ref_barcode['data'] != test_barcode['data']:
                    differences.append({
                        'page_num': page_num,
                        'ref_barcode': ref_barcode['data'],
                        'test_barcode': test_barcode['data']
                    })

        return differences

    def validate_pdf(self, test_pdf_path: str):
        """Основной метод для проверки PDF на соответствие эталону."""

        reference_images = self._convert_pdf_to_images(self.reference_pdf_path)
        reference_text_data = [self._parse_text_data(self._extract_text_from_image(image)) for image in
                               reference_images]
        reference_barcode_data = [self._extract_barcodes_from_image(image) for image in reference_images]

        test_images = self._convert_pdf_to_images(test_pdf_path)
        test_text_data = [self._parse_text_data(self._extract_text_from_image(image)) for image in test_images]
        test_barcode_data = [self._extract_barcodes_from_image(image) for image in test_images]

        text_differences = self._compare_text_data(reference_text_data, test_text_data)

        barcode_differences = self._compare_barcode_data(reference_barcode_data, test_barcode_data)

        report = []

        if text_differences:
            report.append(f"Найдено {len(text_differences)} различий в тексте:")
            for diff in text_differences:
                if 'message' in diff:
                    report.append(f"Страница {diff['page_num']}: {diff['message']}")
                else:
                    report.append(
                        f"Страница {diff['page_num']}: Эталонный текст: "
                        f"'{diff['ref_text']}' - "
                        f"Тестовый текст: '{diff['test_text']}'")
        else:
            report.append("Текст совпадает на всех страницах.")

        if barcode_differences:
            report.append(f"Найдено {len(barcode_differences)} различий в штрихкодах:")
            for diff in barcode_differences:
                if 'message' in diff:
                    report.append(f"Страница {diff['page_num']}: {diff['message']}")
                else:
                    report.append(
                        f"Страница {diff['page_num']}: Эталонный штрихкод:"
                        f" '{diff['ref_barcode']}' - Тестовый штрихкод:"
                        f" '{diff['test_barcode']}'")
        else:
            report.append("Штрихкоды совпадают на всех страницах.")

        if not text_differences and not barcode_differences:
            report.append("PDF соответствует эталону.")

        return report

__all__=()
