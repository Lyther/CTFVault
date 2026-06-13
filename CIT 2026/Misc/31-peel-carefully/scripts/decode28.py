text = b"dOB_c7Bia_Z['~<h)~BC%Z<h%IVE28A==8A)(73)(7]<'^U<(]A<']I\">:F2a_ZW'zVE17E==^/\">eg0dOBidOB_a_Z[)zVE18A==7I==@;)<73==7I\">eRfa_VO'~8S)~<e:ZBC%Z<O%~BC&~8:%$82%48\%4Ze?4Ze?44d2zV21OE(=]I<:8])>8E(?@U)>8/\">_0/d)B?d)<>c7R$a^V\%Hll"

decoded = ""
for b in text:
    if 33 <= b <= 126:
        decoded += chr(33 + ((b - 33 + 47) % 94))
    else:
        decoded += chr(b)

print("ROT47:", decoded)
