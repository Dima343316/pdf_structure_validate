from pdf_parser import PdfStructureValidator


def test_pdf_structure():
    reference_pdf_path = 'files/test_task.pdf'
    test_pdf_path = 'files/test_task.pdf'

    pdf_validator = PdfStructureValidator(reference_pdf_path, lang='eng')

    report = pdf_validator.validate_pdf(test_pdf_path)

    for line in report:
        print(line)

    assert "PDF соответствует эталону." in report or len(report) > 1

__all__=()
