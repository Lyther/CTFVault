import fitz

doc = fitz.open("../files/VF0000000011-Enc.pdf")
doc.authenticate("cherell")

print("Embedded files:", doc.embfile_count())
for i in range(doc.embfile_count()):
    print(doc.embfile_info(i))

# Check annotations
for page_num in range(len(doc)):
    page = doc[page_num]
    for annot in page.annots():
        print(f"Annotation on page {page_num}: {annot.info}")
        
