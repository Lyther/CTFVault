# The Base32 string is:
b32_str = "KVEZ25ATG345M5KXJHLUCMDFKVSZU542OJVSA2RVNMZREEQBGBXRGF2FKLATGYSVORKUSEZWOEYWKVLTKVEZM52VOMJQO4IGN5QWPHRAKV2JM52VONVDM2BVMM2T4DJ6BV7EGIAVJJJTNBRJIZFDICKGYEDDGZLDMZSJY3RAGN"
import base64

try:
    # Add padding
    pad = "=" * ((8 - len(b32_str) % 8) % 8)
    print("Base32 decoded:", base64.b32decode(b32_str + pad))
except Exception as e:
    print("Base32 error:", e)

# The Base64 string is:
b64_str = "VUmddBM2+dZ1V0nXQTBlVWWad5pyayBqNWszEhIBMG8TF0VSwTNiVXRVSRM2cTFlVXNVSZZ3VXMTB3EGb2FnniBVdJZ3VXNqNmg1YzU+DT4NfkMgFUpTNoYpRko0CUbBBjNlY2ZknG4gM1"
try:
    pad = "=" * ((4 - len(b64_str) % 4) % 4)
    print("Base64 decoded:", base64.b64decode(b64_str + pad))
except Exception as e:
    print("Base64 error:", e)

