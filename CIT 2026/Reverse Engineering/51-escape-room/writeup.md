# Writeup: Escape Room

- Category: Reverse Engineering
- Value: 888 pts (113 solves)
- Author: ronnie
- Status: **SOLVED**

## Challenge

We are given a Linux ELF 64-bit statically linked executable named `escaperoom`. Running it presents a terminal menu for a "ROOM 7B EGRESS TERMINAL":

```text
=====================================
  ROOM 7B EGRESS TERMINAL / v2.4.1
=====================================
1. read facility log
2. toggle hallway lights
3. cycle ventilation route
4. rotate camera bus
5. apply door-control patch
6. toggle emergency battery bridge
7. maintenance shell
8. enter door override token
9. status
0. quit
=====================================
```

The goal is to get the correct "door override token" to escape the room and retrieve the flag.

## Solution

By repeatedly reading the facility logs (option 1), we uncover several hints about the correct state the room needs to be in:

1. `[ops/07] Corridor override refuses to arm while hallway lights are ON.`
   -> We must toggle the hallway lights to **OFF** (option 2).
2. `[maint/11] East bypass keeps enough pressure in the service hatch to avoid feedback.`
   -> We must cycle the ventilation route to **east bypass** (option 3).
3. `[cam/03] Camera bus 3 loses sight of the mirror relay for 4.2 seconds each sweep.`
   -> We must rotate the camera bus to **bus 3 / mirror relay** (option 4).
4. `.godhctaw spirt etirw driht ehT .eciwt hctap rood eht ylppA ]20/hctap[`
   -> Reversed, this reads: `[patch/02] Apply the door patch twice. The third write trips watchdog.`
   -> We must apply the door-control patch exactly **twice** (option 5).
5. `[power/06] Bridge emergency battery before maintenance work or the speaker amp browns out.`
   -> We must toggle the emergency battery bridge to **ENGAGED** (option 6) *before* entering the maintenance shell.
6. `[fip/01] Zveebe svefg. Gura uhfu.`
   -> ROT13 decoded, this reads: `[svo/01] Mirror first. Then hush.`
   -> Inside the maintenance shell (option 7), we must run the `mirror` command, followed by the `hush` command.

After performing these actions in order, the room status (option 9) looks like this:

```text
=== room status ===
hallway lights   : OFF
vent route       : east bypass
camera bus       : bus 3 / mirror relay
door patch count : 2
battery bridge   : ENGAGED
inspection mode  : MIRROR READY
alarm speaker    : MUTED
===================
```

With the room in the correct state, we need the override token. By reverse engineering the binary (specifically the `_ZL18buildOverrideTokenv` and `_ZL13roomSignaturev` functions), we can see that the token is generated based on the current state of the room.

We can write a Python script to replicate the token generation algorithm using the correct state values:

```python
import ctypes

def roomSignature():
    # Correct state values
    hallway_lights = 0
    vent_route = 1
    camera_bus = 3
    door_patch_count = 2
    battery_bridge = 1
    inspection_mode = 1
    alarm_speaker = 1

    sig = ctypes.c_uint32(0xa17c3e29)

    sig.value ^= 0x13579bdf if hallway_lights else 0x2468ace0
    sig.value = ((sig.value << 7) | (sig.value >> 25)) & 0xffffffff

    eax = (vent_route + 1) * 0x1f123bb5
    sig.value = (sig.value + eax) & 0xffffffff

    eax = (camera_bus + 3) * 0x45d9f3b
    sig.value ^= eax & 0xffffffff

    eax = (door_patch_count + 5) * 0x27d4eb2d
    sig.value = (sig.value + eax) & 0xffffffff

    sig.value ^= 0xa5a55a5a if battery_bridge else 0x5a5aa5a5
    sig.value = (sig.value + (0x31415926 if inspection_mode else 0x27182818)) & 0xffffffff
    sig.value ^= 0xdeadbeef if alarm_speaker else 0xbad0c0de

    return sig.value

sig = roomSignature()
spice = [0x13, 0x37, 0xc0de, 0xbeef, 0x5a, 0xace, 0x4242, 0x900d, 0x1234, 0x777]
alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'

def buildOverrideToken(sig):
    sig ^= 0x6f70656e
    token = ''
    for i in range(10):
        sig = (sig * 0x19660d) & 0xffffffff
        sig = (sig + spice[i]) & 0xffffffff
        sig = (sig + 0x3c6ef35f) & 0xffffffff
        idx = sig >> 27
        token += alphabet[idx]
        if i == 2 or i == 5:
            token += '-'
    return token

print('Token:', buildOverrideToken(sig))
```

Running this script gives us the token: `RHY-QVT-KAXJ`.

Entering this token into the terminal (option 8) successfully unlocks the door and gives us the flag!

## Flag

```text
CIT{Vc282vlhCxIJ}
```
