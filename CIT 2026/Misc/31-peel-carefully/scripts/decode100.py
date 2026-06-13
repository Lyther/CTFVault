with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "r") as f:
    data = f.read().strip()

triplets = [data[i:i+3] for i in range(0, len(data), 3)]
codons = [t for t in triplets if t != "ATG"]

print("Last 10 codons:", codons[-10:])

# The last 6 codons are:
# TGG TGT TCT TGC GGT TGC GGT
# Wait, that's 7 codons!
# Let's see:
# TGG TGC TGG GGT TTC TGG TGT TCT TGC GGT TGC GGT
# 43 49 54 7B 39 39
# 4 3 4 9 5 4 7 B 3 9 3 9
# TGG(4) TGC(3) TGG(4) GGT(9) TTC(5) TGG(4) TGT(7) TCT(B) TGC(3) GGT(9) TGC(3) GGT(9)
# Wait, "CIT{99" is 6 bytes.
# 6 bytes = 12 hex digits = 12 codons.
# The last 12 codons are exactly "CIT{99"!
# So the flag is "CIT{99...".
# But where is the rest of the flag?
# Is it wrapped around to the beginning?
# Let's check the first few hex digits.
# The hex string starts with:
# 377?754?3226753?3?4?4?4?566?293B5?6?7572544?293B547?4374252B7?20202B7?5?5B26225?5B264029564?44295B407?2956407?552?2?73253?4?4?46566?43742?267420204?5?552?34362?377?753?377?754?3?4?4?4?5?6?43742?2B7?2020267?20207?2?5?2926222020267?552?3445333?4?437?566?2B425?6?29342?4?7572544?297?546?7572536?2B2?54572B2554272B4954274?342?274?342?272737256?43252?7?745B20407?292?2B405?2?2B745B2?7?445?2?2B5?552?4?2?5?375?752?375?292?322645573?4?4349547B3939
# The first hex digits are 37.
# 37 is '7'.
# So the string starts with '7'.
# "CIT{997~uN..."
# Does "CIT{997~uN..." look like a flag?
# No.
