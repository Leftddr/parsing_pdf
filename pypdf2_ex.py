import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
import textract

if len(sys.argv) > 2:
    print('Usage : {} filepath', sys.argv[0])
    sys.exit(1)

if __name__ == '__main__':
    pdfFile = PdfFileReader(open(sys.argv[1], 'rb'))
    docinfo = pdfFile.getDocumentInfo()
    
    page = pdfFile.getPage(0)
    page_content = page.extractText()
    print(page_content)
    

    text = textract.process(sys.argv[1])
    print(text)

    for metaitem in docinfo:
        print(metaitem + ':' + docinfo[metaitem])
