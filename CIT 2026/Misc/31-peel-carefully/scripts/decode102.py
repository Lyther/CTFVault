s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# Wait, what if the string is base85 encoded, but using a different alphabet?
# What if the string is encoded with Ascii85, but the characters are shifted?
# Ascii85 uses !-u (33-117) and z (122).
# Our string has characters from space (32) to ~ (126).
# If we shift the characters by some amount, maybe it becomes Ascii85?
# Let's try shifting the characters.
for shift in range(-94, 94):
    shifted = bytes((c - 32 + shift) % 95 + 32 for c in s3)
    # Check if shifted is valid Ascii85
    if all(33 <= c <= 117 or c == 122 for c in shifted):
        print(f"Shift {shift} gives valid Ascii85!")
        print(shifted)
        import base64
        try:
            print(base64.a85decode(shifted))
        except Exception as e:
            pass

