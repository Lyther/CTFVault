from pypdf import PdfReader, PdfWriter

reader = PdfReader("../files/VF0000000011-Enc.pdf")
reader.decrypt("cherell")

writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

with open("decrypted.pdf", "wb") as f:
    writer.write(f)
