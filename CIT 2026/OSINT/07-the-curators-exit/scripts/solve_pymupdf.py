import fitz

doc = fitz.open("../files/VF0000000011-Enc.pdf")
doc.authenticate("cherell")

for page_num in range(len(doc)):
    page = doc[page_num]
    print(f"--- Page {page_num} ---")
    print(page.get_text())
    
    for img in page.get_images():
        print(f"Image: {img}")

print("Metadata:")
print(doc.metadata)

