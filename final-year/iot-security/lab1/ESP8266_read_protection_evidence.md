# ESP8266EX eFuse / Read-Protection Assessment

**Evidence memo — TP01 IoT Security lab**  
**Date:** 2026-10-20  
**Connected board:** ESP8266EX, 4 MB SPI flash, MAC `84:0d:8e:a5:78:e2`  
**Question:** Can the connected board be configured with `FLASH_CRYPT_CNT=0x1`, `DISABLE_DL_DECRYPT=1`, and `ENABLE_SECURITY_DOWNLOAD=1` to make its firmware read-only?

> **Disclaimer:** This memo is a student technical assessment, not an Espressif publication. It quotes and cites official Espressif documents; those documents are the authoritative sources. No eFuse was burned during this assessment. The board is unchanged.

---

## 1. Executive answer

**No.** The connected chip is an **ESP8266EX**, not an ESP32-family chip. The three named fields do not exist in the ESP8266EX eFuse map:

| Field | Official home | Present on ESP8266EX? |
|---|---|---|
| `FLASH_CRYPT_CNT` | ESP32 (original) | **No** |
| `DISABLE_DL_DECRYPT` | ESP32 (original) | **No** |
| `ENABLE_SECURITY_DOWNLOAD` | ESP32-S3 / S2 / C3 / C2 / H2 | **No** |

The ESP8266EX has **no user-programmable eFuse security block**, **no hardware flash-encryption engine**, **no secure-boot root of trust**, and **no eFuse read-protection lock bits**. Its 128-bit factory eFuse area is used for the MAC address, chip ID, flash-size/calibration data. The official `espefuse` tool rejects the chip as unsupported.

Therefore, the requested bits **cannot be set on this board**, and the board **cannot be made read-only through these eFuses**.

---

## 2. Official documentation evidence

### 2.1 ESP8266EX Datasheet v7.1 (Espressif)

**URL:** https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf

Relevant content:

- **Section 1.2, Table 1-1 (p. 2/26):**
  - **Security:** `WPA/WPA2`
  - **Encryption:** `WEP/TKIP/AES`
  - **Firmware Upgrade:** `UART Download / OTA (via network)`

  These are **Wi-Fi link-security** features. The datasheet does **not** list flash encryption, secure boot, or eFuse read protection.

- **Section 3.1.2, Memory (p. 7/26):** describes SRAM/ROM and states there is no programmable ROM; user programs are stored in external SPI flash.

- **Section 3.1.3, External Flash (p. 8/26):** “ESP8266EX uses external SPI flash to store user programs, and supports up to 16 MB memory capacity theoretically.”

A full-text search of the datasheet returns **0 hits** for:

```
FLASH_CRYPT_CNT
DISABLE_DL_DECRYPT
ENABLE_SECURITY_DOWNLOAD
flash encryption
secure boot
read protection
```

### 2.2 ESP8266 Technical Reference Manual v1.7 (Espressif)

**URL:** https://www.espressif.com/sites/default/files/documentation/esp8266-technical_reference_en.pdf

This is the official 111-page ESP8266 Technical Reference Manual, Version 1.7. A full-text search of the manual returns **0 hits** for all of the following:

```
FLASH_CRYPT_CNT
DISABLE_DL_DECRYPT
ENABLE_SECURITY_DOWNLOAD
flash encryption
secure boot
read protection
```

The manual documents GPIO, SPI, I2C, I2S, UART, PWM, IR, etc. It contains **no eFuse security chapter** and no read-protection mechanism for the external SPI flash.

### 2.3 ESP32 Technical Reference Manual v5.8 (Espressif)

**URL:** https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf

This is the official document that defines the first two fields. They are **ESP32 eFuses**, not ESP8266 eFuses:

- **Chapter 5, eFuse Controller, Table 5.3-1 (p. 91):**
  - `flash_crypt_cnt`, width **7 bits**, bit **[6:0]**, described as governing the **flash encryption/decryption**.
- **Chapter 5, register description (p. 106):**
  - `EFUSE_RD_DISABLE_DL_DECRYPT` — “This field returns the value of `download_dis_decrypt`. (RO)”
- **Chapter 5, register description (p. 109):**
  - `EFUSE_DISABLE_DL_DECRYPT` — “This field programs the value of `download_dis_decrypt`. (R/W)”

Full-text search of the ESP32 TRM: `FLASH_CRYPT_CNT` = **8 hits**, `DISABLE_DL_DECRYPT` = **2 hits**, `ENABLE_SECURITY_DOWNLOAD` = **0 hits**.

### 2.4 ESP32-S3 Technical Reference Manual v1.8 (Espressif)

**URL:** https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf

This is the official document that defines `ENABLE_SECURITY_DOWNLOAD`. It is an **ESP32-S3 eFuse** (also present on S2/C3/C2/H2), not an ESP8266 eFuse:

- **eFuse register description (p. 435):** “`EFUSE_ENABLE_SECURITY_DOWNLOAD` Represents whether secure UART download mode is enabled or disabled (read/write flash only). 1: Enabled. 0: Disabled. (RO)”
- **Functional description (p. 535):** “If this eFuse is set to 1, the secure download mode is enabled, allowing reading, writing, and erasing plaintext flash. However, it does not permit downloading code to flash for direct execution via UART, USB, or SPI interfaces, and register operations are not supported.”

Full-text search of the ESP32-S3 TRM: `ENABLE_SECURITY_DOWNLOAD` = **3 hits**, `FLASH_CRYPT_CNT` = **0 hits**, `DISABLE_DL_DECRYPT` = **0 hits**.

**Note:** the user’s three-field list mixes two different ESP32 generations:

- `FLASH_CRYPT_CNT` + `DISABLE_DL_DECRYPT` → original **ESP32**.
- `ENABLE_SECURITY_DOWNLOAD` → **ESP32-S3/S2/C3/C2/H2**.

No single ESP8266 document defines any of them.

---

## 3. Live-board evidence

The following read-only commands were run against the connected board.

### 3.1 Chip identification

```
$ esptool.py --port /dev/ttyUSB0 flash_id
Chip type:          ESP8266EX
Features:           Wi-Fi, 160MHz
Crystal frequency:  26MHz
MAC:                84:0d:8e:a5:78:e2
Detected flash size: 4MB
```

### 3.2 Raw factory eFuse block

```
$ esptool.py --port /dev/ttyUSB0 dump_mem 0x3FF00050 32 /tmp/opencode/esp_efuse.bin
$ xxd /tmp/opencode/esp_efuse.bin
00000000: 0000 95e2 78a5 0002 00b0 00f2 8e0d 8400
```

Decoded as 32-bit little-endian words:

| Register | Address | Value |
|---|---|---|
| RDATA0 | `0x3FF00050` | `0xE2950000` |
| RDATA1 | `0x3FF00054` | `0x0200A578` |
| RDATA2 | `0x3FF00058` | `0xF200B000` |
| RDATA3 | `0x3FF0005C` | `0x00840D8E` |

These words contain the factory MAC `84:0d:8e:a5:78:e2` and chip ID `0x00A578E2`, plus calibration/flash-size data. They do **not** contain `FLASH_CRYPT_CNT`, `DISABLE_DL_DECRYPT`, or `ENABLE_SECURITY_DOWNLOAD`.

### 3.3 `espefuse` rejects the ESP8266

```
$ espefuse.py --port /dev/ttyUSB0 summary
...
KeyError: 'esp8266'
```

With the older ESP8266-capable esptool 3.3.0:

```
$ espefuse.py --port /dev/ttyUSB0 summary
...
A fatal error occurred: get_efuses: Unsupported chip (ESP8266)
```

### 3.4 Official esptool code reads only the 128-bit factory block

In Espressif’s official `esptool` source, `ESP8266ROM.get_efuses()` reads exactly four 32-bit registers:

```python
result = self.read_reg(0x3ff0005c) << 96
result |= self.read_reg(0x3ff00058) << 64
result |= self.read_reg(0x3ff00054) << 32
result |= self.read_reg(0x3ff00050)
```

Those 128 bits are used for MAC address, chip ID, ESP8285 detection, and flash-size detection. There is no ESP8266 API for burning security eFuses or lock bits.

**Repository:** https://github.com/espressif/esptool

### 3.5 The flash is currently plaintext

The first byte of flash is `0xE9`, the ESP8266 plaintext image magic:

```
00000000: e902 0040 80f4 1040 00f0 1040 600d 0000
```

There is no hardware flash encryption on this board. Even if `FLASH_CRYPT_CNT` existed, setting it to `1` without first encrypting the image and burning the matching key would make the ROM bootloader decrypt garbage and the board would not boot.

---

## 4. Conclusion

1. The connected board is an **ESP8266EX**.
2. The requested bits are **ESP32-family eFuses**:
   - `FLASH_CRYPT_CNT` and `DISABLE_DL_DECRYPT` → original ESP32.
   - `ENABLE_SECURITY_DOWNLOAD` → ESP32-S3/S2/C3/C2/H2.
3. The official ESP8266EX datasheet and 111-page Technical Reference Manual define **none** of these fields, and contain no flash-encryption, secure-boot, or read-protection feature.
4. The chip’s factory eFuse block contains only MAC/chip-ID/calibration data; `espefuse` reports `Unsupported chip (ESP8266)`.
5. **The ESP8266EX cannot be set to read-only using these bits.** There is no supported eFuse mechanism to do so on this chip.

**Recommendation:** If the lab requires these exact bits, use an ESP32-family board that actually implements them (original ESP32 for `FLASH_CRYPT_CNT` + `DISABLE_DL_DECRYPT`; ESP32-S3/S2/C3/C2/H2 for `ENABLE_SECURITY_DOWNLOAD`), and follow the required key/encryption procedure first. If the target is the Arduino Uno (ATmega328P), the correct mechanism is the AVR lock byte `0xC7` (BLB0 mode 4) or `0xC4` (full read protection), programmed through an ISP — not these eFuses.

---

## 5. References

1. Espressif, **ESP8266EX Datasheet**, Version 7.1, 2025.  
   https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf
2. Espressif, **ESP8266 Technical Reference**, Version 1.7.  
   https://www.espressif.com/sites/default/files/documentation/esp8266-technical_reference_en.pdf
3. Espressif, **ESP32 Technical Reference Manual**, Version 5.8.  
   https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf
4. Espressif, **ESP32-S3 Technical Reference Manual**, Version 1.8.  
   https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf
5. Espressif, **esptool** (official repository).  
   https://github.com/espressif/esptool
6. Espressif, **esptool documentation**.  
   https://docs.espressif.com/projects/esptool/en/latest/

---

## Appendix A — Read-only commands used

```bash
# Chip / flash identification
esptool.py --port /dev/ttyUSB0 flash_id

# Dump the ESP8266 factory eFuse block (read-only)
esptool.py --port /dev/ttyUSB0 dump_mem 0x3FF00050 32 /tmp/opencode/esp_efuse.bin
xxd /tmp/opencode/esp_efuse.bin

# Confirm eFuse tool support
espefuse.py --port /dev/ttyUSB0 summary

# Confirm plaintext firmware magic
esptool.py --port /dev/ttyUSB0 read_flash 0 32 /tmp/opencode/esp_head.bin
xxd /tmp/opencode/esp_head.bin

# Full-text search of the official ESP8266 documents
pdftotext -layout esp8266_datasheet.pdf esp8266_datasheet.txt
pdftotext -layout esp8266_trm.pdf esp8266_trm.txt
for t in FLASH_CRYPT_CNT DISABLE_DL_DECRYPT ENABLE_SECURITY_DOWNLOAD \
         "flash encryption" "secure boot" "read protection"; do
    grep -ci "$t" esp8266_datasheet.txt
    grep -ci "$t" esp8266_trm.txt
done
```

## Appendix B — Search results

```
ESP8266 datasheet v7.1:
FLASH_CRYPT_CNT              0
DISABLE_DL_DECRYPT           0
ENABLE_SECURITY_DOWNLOAD     0
flash encryption             0
secure boot                  0
read protection              0

ESP8266 Technical Reference v1.7:
FLASH_CRYPT_CNT              0
DISABLE_DL_DECRYPT           0
ENABLE_SECURITY_DOWNLOAD     0
flash encryption             0
secure boot                  0
read protection              0

ESP32 TRM v5.8:
FLASH_CRYPT_CNT              8
DISABLE_DL_DECRYPT           2
ENABLE_SECURITY_DOWNLOAD     0

ESP32-S3 TRM v1.8:
FLASH_CRYPT_CNT              0
DISABLE_DL_DECRYPT           0
ENABLE_SECURITY_DOWNLOAD     3
```
