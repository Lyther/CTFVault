# What if the original Chinese characters are the key?
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Is it possible that the Chinese characters are Unicode codepoints, and we can map them to something else?
# We found that the hex string of the codepoints is:
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# And we noticed that the first character is '5'.
# What if this is a Base58 encoded string?
import base64

# What if it's a Base85 encoded string?
# We checked, it has characters outside Base85.

# Wait, we found 3 permutations that give a printable ASCII string ending in "CIT{99".
# The 3 strings are:
s1 = b'7\x7fuO2&u1>OM@Vl);QlurTM);TqCt%+~((+~Q[&"Q[&H)VLD)[H~)VHqU,-s%>OMFVmCt.&t((L_U,46*7\x7fu17\x7fuO>OM@QmCt.+~((&q((z Q)&"((&qU,4E3>OC\x7fVl+BQl)4-MurTM)\x7fTlurSl+-TW+%T\'+IT\'M4/\'M4/\'\'7%mC%.\x7ft[(Hq)-+HQ,+t[/zDQ,+_U,O*_7Qu/7Q),2&EW>LCIT{99'
s2 = b'7~uN2&u1?NM@Vl);QlurTM);TqCt%+\x7f((+\x7fQ[&"Q[&H)VLD)[H\x7f)VHqU,-s%?NMFVmCt/&t((L^U,46*7~u17~uN?NM@QmCt/+\x7f((&q((z Q)&"((&qU,4E3?NC~Vl+BQl)4-MurTM)~TlurSl+-TW+%T\'+IT\'M4.\'M4.\'\'7%mC%/~t[(Hq)-+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW?LCIT{99'
s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# What if "CIT{99" is the END of the flag?
# Like "CIT{...99}"? No, there is no '}'.
# What if the flag is "CIT{99" and then some other characters that are not printable?
# No, the string ends exactly there.
# What if the flag is "CIT{99" and the rest of the string is the flag, but reversed?
# "CIT{99" -> 99{TIC
# What if the flag is "CIT{99...}" and it's just wrapped around?
# "CIT{997~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=L}"
# This is a very long flag.
# Is there any other way to decode it?
# What if we decode the hex string as Base64?
# We tried, it failed.

# Let's look at the hex string again:
# 377?754?3226753?3?4?4?4?566?293B5?6?7572544?293B547?4374252B7?20202B7?5?5B26225?5B264029564?44295B407?2956407?552?2?73253?4?4?46566?43742?267420204?5?552?34362?377?753?377?754?3?4?4?4?5?6?43742?2B7?2020267?20207?2?5?2926222020267?552?3445333?4?437?566?2B425?6?29342?4?7572544?297?546?7572536?2B2?54572B2554272B4954274?342?274?342?272737256?43252?7?745B20407?292?2B405?2?2B745B2?7?445?2?2B5?552?4?2?5?375?752?375?292?322645573?4?4349547B3939
# Notice that the hex string has 440 characters.
# But the original hex string from the codepoints has 213 characters!
# Wait!
# 440 characters vs 213 characters.
# What if the 213-character hex string is the payload, and we need to decode it?
# We did that, it gave us:
# b'\x05T\x99\xd7A3o\x9dgUt\x9dt\x13\x06UVY\xa7y\xa7&\xb2\x06\xa3V\xb31! \x13\x06\xf11tU,\x136%WET\x913g\x13\x16UW5T\x99guW10w\x10f\xf6\x16y\xe2\x05WIguW6\xa3f\x83V3S\xe0\xd3\xe0\xd7\xe42\x01T\xa53hb\x94d\xa3@\x94l\x10c6V6fI\xc6\xe2\x035'
# Does this look like a flag? No.

# What if the 213-character hex string is a Base64 string?
# We checked, it has characters outside Base64.
# What if the 213-character hex string is a Base85 string?
# We checked, it has characters outside Base85.

# Let's count the number of Morse code characters again.
# 1320 characters.
# 1320 / 8 = 165 bytes.
# What if we decode the Morse code as binary?
# - = 1, . = 0
