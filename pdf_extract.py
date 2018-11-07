import PyPDF2

pdf_file = open('2018-827.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
info = read_pdf.getDocumentInfo()
print(info)
exit()
number_of_pages = read_pdf.getNumPages()
for i in range(0, number_of_pages):
    page = read_pdf.getPage(i)
    page_content = page.extractText()
    print (page_content.encode('utf-8'))
