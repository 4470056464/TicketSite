import pdfkit
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
# pdfkit.from_string(index.html, 'MyPDF.pdf', configuration=config)

# pdfkit.from_string('hello','string.pdf')


pdfkit.from_file('index.html','file.pdf',configuration=config)
# pdfkit.from_url("http://google.com", "out.pdf")