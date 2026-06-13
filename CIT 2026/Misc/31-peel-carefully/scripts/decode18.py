import collections

text = "GJZTYOZFYTccWBHFaBZYCcHFCFLPXQYHHQYaaODaaOTHWTRHaTYHWTFIHEGXYTcMWNLPDOPHHTUIHPbXGJZFGJZTYTccaNLPDQYHHOFHHZEaHODHHOFIHPSGYTLJWBQVaBHPEcZYCcHJCBZYKBQECKQXCAQTCAcPHAcPHAAGXNLXDJPaHTFHEQTaHQPaHZRaHQUIHTXUGaZHGaHHYOSKYTLTCFJJ"

mapping = {
    'H': ' ',
    'T': 'e',
    'C': 't',
    'Y': 'a',
    'a': 'o',
    'F': 'i',
    'Z': 'n',
    'P': 's',
    'Q': 'h',
    'O': 'r',
    'X': 'd',
    'D': 'l',
    'W': 'u',
    'A': 'm',
    'E': 'c',
    'B': 'g',
    'J': 'y',
    'G': 'w',
    'R': 'v',
    'L': 'f',
    'c': 'p',
    'I': 'k',
    'K': 'b',
    'U': 'x',
    'S': 'j',
    'M': 'q',
    'N': 'z',
    'b': 'w',
    'V': 'w'
}

decoded = "".join(mapping.get(c, c) for c in text)
print(decoded)
