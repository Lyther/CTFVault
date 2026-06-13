import base64

s3 = b'7~uN2&u1=NO@Vl);QlurTO);TqCt%+}((+}Q[&"Q[&H)VLD)[H})VHqU,/s%=NOFVoCt-&t((L^U,46*7~u17~uN=NO@QoCt-+}((&q((z Q)&"((&qU,4E3=NC~Vl+BQl)4/OurTO)~TlurSl+/TW+%T\'+IT\'O4.\'O4.\'\'7%oC%-~t[(Hq)/+HQ,+t[.zDQ,+^U,N*^7Qu.7Q),2&EW=LCIT{99'

# It says incorrect padding. But len(s3) is 220, which is a multiple of 4.
# Wait, base64.b64decode ignores characters that are not in the base64 alphabet!
# The base64 alphabet is A-Z, a-z, 0-9, +, /.
# s3 contains characters like ~, &, =, @, ;, (, ), [, ], ", *, ', ., ,, {, }.
# These are NOT in the base64 alphabet.
# So base64.b64decode strips them out!
# The remaining characters have a length that is not a multiple of 4, so it complains about padding.
# This means s3 is NOT a base64 encoded string!

# What if s3 is just the flag?
# "CIT{99..."
# But the string is 220 characters long.
# And it looks like gibberish.
# Wait, look at the characters:
# 7 ~ u N 2 & u 1 = N O @ V l ) ; Q l u r T O ) ; T q C t % + } ( ( + } Q [ & " Q [ & H ) V L D ) [ H } ) V H q U , / s % = N O F V o C t - & t ( ( L ^ U , 4 6 * 7 ~ u 1 7 ~ u N = N O @ Q o C t - + } ( ( & q ( ( z   Q ) & " ( ( & q U , 4 E 3 = N C ~ V l + B Q l ) 4 / O u r T O ) ~ T l u r S l + / T W + % T ' + I T ' O 4 . ' O 4 . ' ' 7 % o C % - ~ t [ ( H q ) / + H Q , + t [ . z D Q , + ^ U , N * ^ 7 Q u . 7 Q ) , 2 & E W = L C I T { 9 9
# This is a string of 220 characters.
# What if it's ROT47 encoded?
# We tried that, it gave gibberish.
# What if it's XORed with a repeating key?
# Let's try to break repeating key XOR.
