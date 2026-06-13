b = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# Decode ROT47
decoded = ""
for x in b:
    if 33 <= x <= 126:
        decoded += chr(33 + ((x - 33 + 47) % 94))
    else:
        decoded += chr(x)

print("ROT47:", decoded)

# Is it base64?
import base64
try:
    print("Base64:", base64.b64decode(decoded + "==="))
except Exception as e:
    print("Base64 error:", e)

