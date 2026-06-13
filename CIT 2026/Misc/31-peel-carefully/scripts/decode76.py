# The output is:
# b'7quA2&u8?AJ@Vn);XnurTJ);TxCt%+\x7f--+\x7fX[&"X[&M)VND)[M\x7f)VMxU.*s%?AJFVjCt/&t--NQU.46,7qu87quA?AJ@XjCt/+\x7f--&x--| X)&"--&xU.4E3?ACqVn+BXn)4*JurTJ)qTnurSn+*TW+%T\'+IT\'J4!\'J4!\'\'7%jC%/qt[-Mx)*+MX.+t[!|DX.+QU.A,Q7Xu!7X).2&EW?NCIT{99'
# Wait! It's a ROT47 encoded string!
# Let's decode it with ROT47!
b = b'7quA2&u8?AJ@Vn);XnurTJ);TxCt%+\x7f--+\x7fX[&"X[&M)VND)[M\x7f)VMxU.*s%?AJFVjCt/&t--NQU.46,7qu87quA?AJ@XjCt/+\x7f--&x--| X)&"--&xU.4E3?ACqVn+BXn)4*JurTJ)qTnurSn+*TW+%T\'+IT\'J4!\'J4!\'\'7%jC%/qt[-Mx)*+MX.+t[!|DX.+QU.A,Q7Xu!7X).2&EW?NCIT{99'

decoded = ""
for x in b:
    if 33 <= x <= 126:
        decoded += chr(33 + ((x - 33 + 47) % 94))
    else:
        decoded += chr(x)

print(decoded)
