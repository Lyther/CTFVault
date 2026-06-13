# The string ends with "CIT{99".
# Wait. What if the string is base64 encoded, and we just need to decode it?
# The string is:
s = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
# It has characters like '~', '&', '=', '@', ';', '(', ')', '%', '[', ']', '"', '*', '+', '-', '.', '/', ':', '<', '>', '?', '\\', '^', '_', '`', '{', '|', '}'
# This is NOT base64.
# This is NOT base32.
# This is NOT base85. Base85 uses !-u. It does not use ~, |, }.
# This is NOT ascii85. Ascii85 uses !-u and z. It does not use ~, |, }.
# Wait! Base85 uses !-u. Ascii85 uses !-u.
# But this string has '~', '|', '}', '{'.
# What encoding uses these characters?
# Base91? Base92? Base94? Base122?
# ROT47 uses 33-126.
# If we apply ROT47 to it, we get:
# fOF}aUF`l}~o'=Xj"=FC%~Xj%BrETZNWWZN",UQ",UwX'{sX,wNX'wB&[^DTl}~u'@rE\UEWW{/&[ceYfOF`fOF}l}~o"@rE\ZNWWUBWWK "XUQWWUB&[ctbl}rO'=Zq"=Xc^~FC%~XO%=FC$=Z^%(ZT%VZx%V~c]V~c]VVfT@rT\OE,WwBX^Zw"[ZE,]Ks"[Z/&[}Y/f"F]f"X[aUt(l{rx%Lhh
# This also has '~', '`', '{', '}', '|', etc.

# Wait! The string ends with "CIT{99".
# If the string ends with "CIT{99", maybe the flag is literally "CIT{99..."?
# What if the flag is "CIT{99..." and the rest of the flag is at the BEGINNING of the string?
# "CIT{997~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=L"
# But this has characters like '~', '&', '=', '@', ';', '(', ')', '%', '[', ']', '"', '*', '+', '-', '.', '/', ':', '<', '>', '?', '\\', '^', '_', '`', '{', '|', '}'
# Is a flag allowed to have these characters?
# Yes, but usually flags are alphanumeric + underscores.
# The challenge says: "One layer at a time, the message reveals itself... can you read it?"
# "It's all there, just buried."
# What if the string is encrypted with a repeating key XOR?
# If we know the plaintext starts with "CIT{", we can find the key!
# But wait, "CIT{" is already in the ciphertext!
# If "CIT{" is in the ciphertext, it means the key for that part is 0!
# Or maybe it's not encrypted anymore!
