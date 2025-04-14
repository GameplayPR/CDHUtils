import fitz
import base64
from io import BytesIO

def convert_pdf_to_image(pdf_bytes):
    images_base64 = []

    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(dpi=200)

        buffer = BytesIO(pix.tobytes("png"))
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        images_base64.append(encoded_image)

    return images_base64
