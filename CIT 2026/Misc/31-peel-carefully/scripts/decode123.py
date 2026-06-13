hex_str = "377075403226753C3A404D48566E293B5C6E7572544D293B547C4374252B7A20202B7A5C5B26225C5B264029564E44295B407A2956407C552E2D73253A404D46566D43742A267420204E50552E34362F3770753C377075403A404D485C6D43742A2B7A2020267C20207F285C2926222020267C552E3445333A404370566E2B425C6E29342D4D7572544D2970546E7572536E2B2D54572B2554272B4954274D3420274D3420272737256D43252A70745B20407C292D2B405C2E2B745B207F445C2E2B50552E402F50375C7520375C292E322645573A4E4349547B3939"

print("Has 7D:", "7D" in hex_str)
print("Has 7d:", "7d" in hex_str)

# What if the mapping is slightly different?
# We used a mapping that gave us a printable ASCII string.
# But there are 3 such mappings!
# Let's check if any of them has '}' (7D).
# We checked before, s3 has '}' (7D).
# Let's look at s3 again:
s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
print("Has } in s3:", b'}' in s3)

# If s3 has '}', then maybe the flag is "CIT{99...}" and it ends with '}'?
# Let's find the '}' in s3.
indices = [i for i, c in enumerate(s3) if c == ord('}')]
print("Indices of }:", indices)

# The indices are 30, 34, 50, 98.
# The string is 220 characters long.
# If the flag starts at 214 ("CIT{") and ends at 30, it would be 37 characters long.
# "CIT{997~uN2&u1=NO@Vl);QlurTO);TqCt%+}"
# Does this look like a flag?
# It has '~', '&', '=', '@', ';', ')', '%', '+'.
# It's possible, but unlikely.

# What if the string is Base85 encoded?
# We checked, it has characters outside Base85.

