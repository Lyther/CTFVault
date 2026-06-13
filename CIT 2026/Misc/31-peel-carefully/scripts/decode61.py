hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# What if we just decode it as hex but skip the first character?
# 5 54 99 d7 41 33 6f 9d ...
data = bytes.fromhex(hex_str[1:])
print(data)

# What if we decode it as hex but append a 0?
data = bytes.fromhex(hex_str + "0")
print(data)

