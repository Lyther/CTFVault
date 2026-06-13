import fitz

doc = fitz.open("../files/VF0000000011-Enc.pdf")
doc.authenticate("cherell")
doc.save("decrypted_fitz.pdf")
