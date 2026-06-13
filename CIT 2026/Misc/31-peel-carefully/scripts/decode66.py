# The hex string is "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"
hex_str = "55499d741336f9d6755749d741306555659a779a726b206a356b33121201306f13174552c133625574554913367131655573554996775573130771066f61679e205574967755736a36683563353e0d3e0d7e4320154a53368629464a340946c10633656366649c6e20335"

# What if we take the integer value and convert it to bytes?
val = int(hex_str, 16)
b = val.to_bytes((val.bit_length() + 7) // 8, 'big')

# What if we XOR the bytes with a key?
# Let's try to find "CIT{" in the XORed bytes.
for i in range(len(b) - 3):
    key = bytes([b[i] ^ ord('C'), b[i+1] ^ ord('I'), b[i+2] ^ ord('T'), b[i+3] ^ ord('{')])
    # Check if the key repeats
    if key[0] == key[1] == key[2] == key[3]:
        print(f"Found single-byte XOR key {key[0]} at {i}")
    
    # Check if it's a 4-byte repeating key
    # We can just print all possible keys and see if any look like words
    # Actually, let's just print the first few bytes of the key
    if all(32 <= k <= 126 for k in key):
        # print(f"Possible key at {i}: {key}")
        pass

