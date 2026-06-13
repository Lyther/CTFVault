# Let's go back to the hex string that ended with "CIT{99"
# The string was:
# 377?754?3226753?3?4?4?4?566?293B5?6?7572544?293B547?4374252B7?20202B7?5?5B26225?5B264029564?44295B407?2956407?552?2?73253?4?4?46566?43742?267420204?5?552?34362?377?753?377?754?3?4?4?4?5?6?43742?2B7?2020267?20207?2?5?2926222020267?552?3445333?4?437?566?2B425?6?29342?4?7572544?297?546?7572536?2B2?54572B2554272B4954274?342?274?342?272737256?43252?7?745B20407?292?2B405?2?2B745B2?7?445?2?2B5?552?4?2?5?375?752?375?292?322645573?4?4349547B3939
# Wait, "CIT{99" is 43 49 54 7B 39 39.
# If the flag is "CIT{99...", then the string is NOT reversed, but the flag is at the END of the string!
# Wait, if the flag is at the end of the string, maybe the rest of the flag is missing?
# Or maybe the flag is short? "CIT{99}"?
# Let's look at the actual bytes of the string we found:
# b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
# Notice the end: `CIT{99`
# But wait, what if the flag is NOT at the end?
# What if the string is just a base64 encoded string, and we just happened to find "CIT{" in it?
# No, "CIT{" in hex is 43 49 54 7B.
# That's exactly the hex values for C, I, T, {.
# And it's at the end of the hex string!
# Wait!
# The hex string is 440 characters long.
# 440 characters = 220 bytes.
# If it ends with "CIT{99", then the last bytes are C, I, T, {, 9, 9.
# But wait!
# If the hex string is 440 characters long, and it ends with "4349547B3939",
# then the bytes are literally the ASCII string!
# The hex string IS the ASCII string!
# Let's decode the whole hex string as ASCII!
# We did that! It gave us:
# b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'
# This is a string of 220 characters!
# And it ends with "CIT{99".
# Wait, where is the '}'?
# The string doesn't end with '}'. It ends with '99'.
# What if the string is reversed?
# If the string is reversed, "CIT{99" reversed is "99{TIC".
# But it's NOT reversed in the hex string.
# What if the original codons were reversed?
