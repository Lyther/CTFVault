# Let's look at the mapping again.
# We found 3 permutations that give a printable ASCII string ending in "CIT{99".
# The 3 strings are:
s1 = b'7\x7fuO2&u1>OM@Vl);QlurTM);TqCt%+~((+~Q[&"Q[&H)VLD)[H~)VHqU,-s%>OMFVmCt.&t((L_U,46*7\x7fu17\x7fuO>OM@QmCt.+~((&q((z Q)&"((&qU,4E3>OC\x7fVl+BQl)4-MurTM)\x7fTlurSl+-TW+%T\'+IT\'M4/\'M4/\'\'7%mC%.\x7ft[(Hq)-+HQ,+t[/zDQ,+_U,O*_7Qu/7Q),2&EW>LCIT{99'
s2 = b'7~uN2&u1?NM@Vl);QlurTM);TqCt%+\x7f((+\x7fQ[&"Q[&H)VLD)[H\x7f)VHqU,-s%?NMFVmCt/&t((L^U,46*7~u17~uN?NM@QmCt/+\x7f((&q((z Q)&"((&qU,4E3?NC~Vl+BQl)4-MurTM)~TlurSl+-TW+%T\'+IT\'M4.\'M4.\'\'7%mC%/~t[(Hq)-+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW?LCIT{99'
s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# What if these strings are base85 encoded?
# We checked, they have characters outside base85.
# What if these strings are Base64 encoded?
# We checked, they have characters outside base64.
# What if these strings are hex encoded?
# No.

# What if the string is a URL?
# What if the string is a file path?
# What if the string is a piece of code?
# What if the string is a piece of text that has been compressed?
# What if the string is a piece of text that has been encrypted with AES?
# If it's encrypted with AES, it would be random bytes, not printable ASCII.
# The fact that it's printable ASCII means it's likely a text-based encoding.

# What if the string is a piece of text that has been encoded with a custom base encoding?
# Base 52?
# Base 52 encoding uses 52 characters.
# Our string has 52 unique characters!
# This is a strong hint that it might be Base52 encoded!
# How does Base52 encoding work?
# Base52 uses A-Z, a-z.
# But our string has characters like '~', '&', '=', '@', ';', '(', ')', '%', '[', ']', '"', '*', '+', '-', '.', '/', ':', '<', '>', '?', '\\', '^', '_', '`', '{', '|', '}'.
# So it's NOT Base52.

# What if the string is a piece of text that has been encoded with a substitution cipher, but the alphabet is NOT A-Z?
# What if the alphabet is the 52 unique characters in the string?
# If it's a substitution cipher, we can break it!
# But we tried to break it with simulated annealing, and it failed.
# Why did it fail?
# Maybe the text is NOT English!
# Maybe the text is a piece of code!
# Maybe the text is a URL!
# Maybe the text is a base64 string!
# Wait! If the text is a base64 string, it would have 64 unique characters.
# But our string has 52 unique characters.
# A base64 string can have 52 unique characters if it's short.
# But our string is 220 characters long.
# If it's a base64 string, it would probably have more than 52 unique characters.
