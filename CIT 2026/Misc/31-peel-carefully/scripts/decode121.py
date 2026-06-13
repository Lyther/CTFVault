# The hex string is:
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if we just try to decode it as a Vigenere cipher?
# We tried, it failed.

# What if we decode it as a substitution cipher?
# We tried, it failed.

# What if we decode it as a transposition cipher?
# We tried, it failed.

# What if we decode it as a custom base encoding?
# We tried, it failed.

# Let's look at the hex string again.
# 55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335
# What if we convert the hex string to an integer, and then to a string of base 10 digits?
# Let's try that!
val = int("55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335", 16)
print(str(val))

# What if we convert the hex string to an integer, and then to a string of base 8 digits?
print(oct(val)[2:])

# What if we convert the hex string to an integer, and then to a string of base 2 digits?
print(bin(val)[2:])

# What if we convert the hex string to an integer, and then to a string of base 36 digits?
def base36encode(number):
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36
    return base36 or alphabet[0]

print(base36encode(val))

# What if we convert the hex string to an integer, and then to a string of base 62 digits?
def base62encode(number):
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    base62 = ''
    while number:
        number, i = divmod(number, 62)
        base62 = alphabet[i] + base62
    return base62 or alphabet[0]

print(base62encode(val))

