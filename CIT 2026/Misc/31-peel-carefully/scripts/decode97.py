s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# Look at the string again.
# It ends with "CIT{99".
# Wait, "CIT{99" is 6 characters.
# What if the string is base85 encoded? No.
# What if the string is encoded with a custom alphabet?
# What if we just try to decode it as Base64 but with a custom alphabet?
# But we don't know the alphabet.

# Let's look at the original text again.
text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"
# Is there any other way to extract data from it?
# We extracted the codepoints, and concatenated their hex representations to get a 213-character hex string.
# What if we concatenate their decimal representations?
# What if we concatenate their binary representations?
# We did that, it was 900 bits (or 1050 bits).

# What if the hex string is just a big number, and we convert it to base 58?
import base58
try:
    val = int("55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335", 16)
    b = val.to_bytes((val.bit_length() + 7) // 8, 'big')
    print(base58.b58encode(b))
except Exception as e:
    pass

# What if the hex string is a sequence of bytes, and we decode it with base58?
try:
    b = bytes.fromhex("055499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335")
    print(base58.b58decode(b))
except Exception as e:
    pass
