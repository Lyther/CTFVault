# Let's look at the mapping again.
# We found 3 permutations that give a printable ASCII string ending in "CIT{99".
# The 3 strings are:
s1 = b'7\x7fuO2&u1>OM@Vl);QlurTM);TqCt%+~((+~Q[&"Q[&H)VLD)[H~)VHqU,-s%>OMFVmCt.&t((L_U,46*7\x7fu17\x7fuO>OM@QmCt.+~((&q((z Q)&"((&qU,4E3>OC\x7fVl+BQl)4-MurTM)\x7fTlurSl+-TW+%T\'+IT\'M4/\'M4/\'\'7%mC%.\x7ft[(Hq)-+HQ,+t[/zDQ,+_U,O*_7Qu/7Q),2&EW>LCIT{99'
s2 = b'7~uN2&u1?NM@Vl);QlurTM);TqCt%+\x7f((+\x7fQ[&"Q[&H)VLD)[H\x7f)VHqU,-s%?NMFVmCt/&t((L^U,46*7~u17~uN?NM@QmCt/+\x7f((&q((z Q)&"((&qU,4E3?NC~Vl+BQl)4-MurTM)~TlurSl+-TW+%T\'+IT\'M4.\'M4.\'\'7%mC%/~t[(Hq)-+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW?LCIT{99'
s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# What if these strings are Base92 encoded?
# Base92 uses 92 printable characters.
# It uses characters from '!' (33) to '~' (126), except '-'.
# But our strings contain '-'.
# So it's not base92.

# What if these strings are encoded with a custom base encoding?
# Let's count the number of unique characters in s3.
print("Unique chars in s3:", len(set(s3)))
# 52 unique characters.
# What if it's a Vigenere cipher?
# Let's try to break Vigenere cipher on s3.
# Let's assume the key length is between 1 and 20.
def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    for i, c in enumerate(ciphertext):
        if 32 <= c <= 126:
            k = key[i % len(key)]
            plaintext += chr((c - 32 - (k - 32)) % 95 + 32)
        else:
            plaintext += chr(c)
    return plaintext

# We know the last 6 characters are "CIT{99".
# The ciphertext for the last 6 characters is also "CIT{99".
# This means the key for the last 6 characters is "      " (spaces, which correspond to 0 shift).
# If the key is a repeating sequence, and the last 6 characters have key "      ",
# then the key must be "      " everywhere!
# But the rest of the string is gibberish.
# This means the string is NOT a Vigenere cipher.

# What if the string is a substitution cipher?
# We tried that.

# What if the string is a piece of code?
# What if the string is a URL?
# What if the string is a base64 string, but it's padded with "CIT{99"?
# Let's check if the string before "CIT{99" is a valid base64 string.
s3_prefix = s3[:-6]
print("Prefix length:", len(s3_prefix))
# 214 characters.
# 214 is not a multiple of 4.
# 214 % 4 = 2.
# So it could be a base64 string without padding.
# Let's try to decode it as base64.
import base64
try:
    print(base64.b64decode(s3_prefix + b"=="))
except Exception as e:
    print("Base64 error:", e)

