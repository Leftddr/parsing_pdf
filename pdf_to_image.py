from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
import pytesseract
from PIL import Image
import sys

if len(sys.argv) < 2:
    print('Usage : {} filepath'.format(sys.argv[0]))
    sys.exit(1)

if __name__ == '__main__':
    
    name_list = []
    pdfFile = PdfFileReader(open(sys.argv[1], 'rb'))

    for cur in range(pdfFile.numPages):
        try:
            pdfFile.getPage(cur)
        except IndexError:
            break
        pages = convert_from_path(sys.argv[1], first_page = cur, last_page = cur + 1)
        for page in pages:
            page.save(str(cur) + '.jpg', 'JPEG')
            name_list.append(str(cur) + '.jpg')
    
    out_name = 'output'
    for cur, filename in enumerate(name_list):
        fp = open(str(cur) + '_' + out_name + '.txt', 'w')
        text = str(pytesseract.image_to_string(Image.open(filename)))
        fp.write(text)
        fp.close()


