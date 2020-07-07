from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, HTMLConverter, XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.image import ImageWriter
from io import StringIO
import sys

if len(sys.argv) < 3:
    print('Usage : {} inputfile outputfile'.format(sys.argv[0]))
    exit(1)

def convert_pdf_to_txt():
    rscrmgr = PDFResourceManager(caching = True)
    outfp = open(sys.argv[2] + '.txt', 'w')
    #codec = 'utf-8'
    laparams = LAParams()
    imagewriter = None

    device = TextConverter(rscrmgr, outfp, laparams = laparams, imagewriter = imagewriter)

    fp = open(sys.argv[1], 'rb')

    interpreter = PDFPageInterpreter(rscrmgr, device)

    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    rotation = 0

    for page in PDFPage.get_pages(fp, pagenos, maxpages = maxpages, password = password, caching = caching, check_extractable = True):
        page.rotate = (page.rotate + rotation) % 360
        interpreter.process_page(page)

    fp.close()
    outfp.close()
    device.close()

def convert_pdf_to_html():
    rsrcmgr = PDFResourceManager(caching = True)
    outfp = open(sys.argv[2] + '.html', 'w')
    scale = 1
    laparams = LAParams()
    layoutmode = 'normal'
    imagewriter = None
    pagenos = set()
    maxpages = 0
    password = ""
    caching = True
    rotation = 0

    device = HTMLConverter(rsrcmgr, outfp, scale = scale, layoutmode = layoutmode, laparams = laparams, imagewriter = imagewriter)

    fp = open(sys.argv[1], 'rb')

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos, maxpages = maxpages, password = password, caching = caching, check_extractable = True):
        page.rotate = (page.rotate + rotation) % 360
        interpreter.process_page(page)
    
    outfp.close()
    fp.close()

if __name__ == '__main__':
    convert_pdf_to_txt()
    convert_pdf_to_html()

    