# If the string ends with CIT{99, maybe the flag is reversed?
# Let's reverse the string!
s = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
print(s[::-1])

# What if it's base64 encoded?
# 99{TICL=WE&2,)Q7.uQ7^*N,U^+!QDz.[t+,QH+/)qH([t~-%Co%7\'\'.4O\'.4O\'TI+\'T%+WT/+lSrulT~)OTruO/4)lQB+lV~CN=3E4,Uq&(("&()Q z((q&((}+-tCoQ@ON=Nu~7*64,U^L((t&-tCoFVON=%s/,UqHV)}H)[DLV)H[&"Q"&[Q}+((}+%tCqT;)OTrulQ;)lV@ON=1u&2Nu~7'
# No.

# Wait! The string is 220 characters long.
# It ends with CIT{99.
# Is it possible that the flag is just "CIT{99..." and it wraps around?
# "CIT{997~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=L"
# No, that doesn't look like a flag.

# What if we apply ROT47 to the string?
decoded = ""
for x in s:
    if 33 <= x <= 126:
        decoded += chr(33 + ((x - 33 + 47) % 94))
    else:
        decoded += chr(x)
print("ROT47:", decoded)
