# Let's look at the mapping again.
# We found 3 permutations that give a printable ASCII string ending in "CIT{99".
# The 3 strings are:
s1 = b'7\x7fuO2&u1>OM@Vl);QlurTM);TqCt%+~((+~Q[&"Q[&H)VLD)[H~)VHqU,-s%>OMFVmCt.&t((L_U,46*7\x7fu17\x7fuO>OM@QmCt.+~((&q((z Q)&"((&qU,4E3>OC\x7fVl+BQl)4-MurTM)\x7fTlurSl+-TW+%T\'+IT\'M4/\'M4/\'\'7%mC%.\x7ft[(Hq)-+HQ,+t[/zDQ,+_U,O*_7Qu/7Q),2&EW>LCIT{99'
s2 = b'7~uN2&u1?NM@Vl);QlurTM);TqCt%+\x7f((+\x7fQ[&"Q[&H)VLD)[H\x7f)VHqU,-s%?NMFVmCt/&t((L^U,46*7~u17~uN?NM@QmCt/+\x7f((&q((z Q)&"((&qU,4E3?NC~Vl+BQl)4-MurTM)~TlurSl+-TW+%T\'+IT\'M4.\'M4.\'\'7%mC%/~t[(Hq)-+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW?LCIT{99'
s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# What if this is a Base91 encoded string?
# Base91 uses 91 characters from ASCII 33 to 126.
# It uses all printable characters except -, ', \, and maybe some others.
# Let's check if the strings contain any of those.
print("s1 contains '-':", b'-' in s1)
print("s2 contains '-':", b'-' in s2)
print("s3 contains '-':", b'-' in s3)

# They all contain '-'. Base91 alphabet:
# A-Z, a-z, 0-9, !#$%&()*+,./:;<=>?@[]^_`{|}~"
# It does NOT use -, ', \, .
# But our strings contain '-' and '\''.
# So it's not base91.

# What if it's base92?
# What if it's base85?
# Base85 alphabet: 0-9, A-Z, a-z, !#$%&()*+-;<=>?@^_`{|}~
# Wait, Base85 has multiple alphabets.
# Ascii85 uses !-u (33-117) and z.
# Z85 uses 0-9, a-z, A-Z, ., -, :, +, =, ^, !, /, *, ?, &, <, >, (, ), [, ], {, }, @, %, $, #.
# Let's check if our strings contain characters outside Z85.
z85_chars = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
for s in [s1, s2, s3]:
    for c in s:
        if c not in z85_chars:
            print(f"Char '{chr(c)}' not in Z85")
            break
    else:
        print("Valid Z85!")

