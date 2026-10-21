# 🔬 TP 01 — Firmware Reading via UART (Arduino Uno)

## Full Lab Execution Plan

> **Module**: Embedded Systems Security
> **Duration**: 2h30 – 3h
> **Platform**: Arduino Uno / ATmega328P
> **Approach**: Pedagogical, experimental, and defensive

---

## 📋 Prerequisites

### Hardware

| Item | Details |
|------|---------|
| 1× Arduino Uno board | ATmega328P-based (the target board you own or have authorization to use) |
| 1× USB Type-B cable | Standard Arduino USB cable (USB-A to USB-B) |
| 1× Computer | Windows, Linux, or macOS |
| (Optional) LED / sensor | To observe behavioral changes after firmware modification |

### Software

| Software | Purpose | Installation |
|----------|---------|-------------|
| **Arduino IDE** | Compile & upload sketches | [arduino.cc/en/software](https://www.arduino.cc/en/software) — install for your OS |
| **avrdude** | Read/write Flash via bootloader protocol | Bundled with Arduino IDE, or install separately (Linux: `sudo apt install avrdude` / `sudo dnf install avrdude`) |
| **avr-objcopy** (binutils-avr) | Convert Intel HEX → raw binary | Linux: `sudo apt install binutils-avr` / `sudo dnf install avr-binutils` — on Windows/macOS, bundled with Arduino IDE toolchain |
| **xxd** | Hex dump viewer | Pre-installed on Linux/macOS; Windows: use HxD or another hex editor |
| **sha256sum** | Hash comparison | Pre-installed on Linux; macOS: `shasum -a 256`; Windows: `Get-FileHash` in PowerShell |
| **Serial Monitor** | Observe UART output | Built into Arduino IDE (Tools → Serial Monitor) |

### Knowledge Prerequisites

- Basic understanding of what a microcontroller is
- Familiarity with the Arduino IDE (uploading sketches)
- Basic command-line / terminal usage
- Understanding of serial communication concepts (baud rate, TX/RX)

---

## 🧠 Phase 1 — Understand the Chain (Theory — ~20 min)

### Step 1.1 — Study the Architecture

Before touching hardware, understand the full communication chain:

```
PC (avrdude) → USB cable → USB-to-Serial chip (ATmega16U2) → UART (TX/RX) → Bootloader → Flash Memory
```

**Read and internalize these three key concepts:**

| Concept | Definition |
|---------|-----------|
| **UART** | Asynchronous serial interface. Base signals: TX (transmit), RX (receive), GND (ground reference). Baud rate, data bits, parity, and stop bits must match on both ends. |
| **Bootloader** | Small program executed at startup, before the main application. On Arduino Uno, it receives a new program from the PC without needing an external programmer. |
| **Flash Memory** | Stores the machine code. Reading it does NOT give you the original `.ino` source — you get compiled bytes, sometimes padded with unused zones. |

> [!IMPORTANT]
> Opening the Serial Monitor does **NOT** show the firmware. It only displays data that the program or bootloader **chooses** to send.

### Step 1.2 — Answer Pre-Lab Questions (mentally or in notes)

- What is the difference between UART, JTAG/SWD, and ISP?
- Why doesn't a UART port automatically mean you can read firmware?
- What role does the bootloader play in enabling firmware reading?

---

## ⚙️ Phase 2 — Prepare the Board (~20 min)

### Step 2.1 — Connect the Arduino

1. Plug the Arduino Uno into your computer via the USB cable.
2. Open the Arduino IDE.
3. Go to **Tools → Board** and select **Arduino Uno**.
4. Go to **Tools → Port** and select the correct serial port:
   - **Windows**: `COM3`, `COM4`, etc.
   - **Linux**: `/dev/ttyACM0` or `/dev/ttyUSB0`
   - **macOS**: `/dev/cu.usbmodem...`

> [!TIP]
> On Linux, if you get a permission error, add your user to the `dialout` group:
> ```bash
> sudo usermod -aG dialout $USER
> ```
> Then log out and log back in.

### Step 2.2 — Upload the Demo Sketch (Version A)

Create a new sketch in Arduino IDE and paste:

```cpp
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("TP Firmware UART - version A");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}
```

1. Click **Upload** (→ button) and wait for "Done uploading."
2. The built-in LED should start blinking (500ms on / 500ms off).

### Step 2.3 — Verify Serial Output

1. Open **Tools → Serial Monitor**.
2. Set the baud rate to **9600** (bottom-right dropdown).
3. Press the **Reset** button on the Arduino board.
4. You should see: `TP Firmware UART - version A`
5. **Close the Serial Monitor** when done (important for next steps!).

> [!NOTE]
> Record the port name (e.g., `/dev/ttyACM0`) — you'll need it for avrdude commands.

---

## 🔧 Phase 3 — Manipulations (~1h 30min)

### Manipulation 1 — Observe UART Communication (~15 min)

**Goal**: Understand what UART reveals (and what it doesn't).

1. **Connect** the board via USB.
2. **Open** the Serial Monitor (9600 baud).
3. **Reset** the board (press the physical reset button).
4. **Record** all visible messages.
5. **Note** that these messages are **voluntarily sent** by the application — this is NOT the firmware content.

**What to write in your report:**
- The exact message(s) seen in the Serial Monitor.
- Explanation: the Serial Monitor shows application output, not Flash memory contents.
- Security interpretation: UART output reveals intentional data; firmware extraction requires a different mechanism.

---

### Manipulation 2 — Read Flash Memory with avrdude (~20 min)

**Goal**: Use the bootloader to perform an authorized read of the entire Flash memory.

> [!WARNING]
> **Close the Serial Monitor** before running avrdude! Both cannot use the serial port simultaneously.

**Run the following command** (adapt the port to your system):

```bash
# Linux
avrdude -p m328p -c arduino -P /dev/ttyACM0 -b 115200 -U flash:r:firmware.hex:i

# Windows
avrdude -p m328p -c arduino -P COM3 -b 115200 -U flash:r:firmware.hex:i

# macOS
avrdude -p m328p -c arduino -P /dev/cu.usbmodem* -b 115200 -U flash:r:firmware.hex:i
```

**Parameter breakdown:**

| Parameter | Meaning |
|-----------|---------|
| `-p m328p` | Target MCU: ATmega328P |
| `-c arduino` | Programmer type: Arduino bootloader |
| `-P /dev/ttyACM0` | Serial port (adapt to your system) |
| `-b 115200` | Baud rate for bootloader communication |
| `-U flash:r:firmware.hex:i` | Operation: **r**ead **flash**, save to `firmware.hex`, format **i**ntel HEX |

**Verification checklist:**

- [ ] `firmware.hex` file was created in the current directory
- [ ] Check file size: `ls -la firmware.hex` (should be several KB)
- [ ] avrdude reported a successful read (look for "bytes of flash read")
- [ ] Open `firmware.hex` in a text editor — lines should start with `:` (Intel HEX format)

```bash
# Quick verification
ls -la firmware.hex
head -5 firmware.hex
```

---

### Manipulation 3 — Conversion and Inspection (~20 min)

**Goal**: Convert the Intel HEX file to raw binary and inspect the contents.

#### Step 3.1 — Convert HEX to Binary

```bash
avr-objcopy -I ihex -O binary firmware.hex firmware.bin
```

#### Step 3.2 — Inspect the Binary

```bash
# View first bytes as hex dump
xxd firmware.bin | head -20

# Check the file size
ls -la firmware.bin

# Search for readable strings (like our "version A" message)
strings firmware.bin | grep -i "version"
strings firmware.bin | grep -i "TP"
```

**What to observe:**
- The binary file contains **compiled machine code** (not human-readable C/C++)
- You may find the string `"TP Firmware UART - version A"` embedded in the binary (string literals are stored in Flash)
- Most of the content is opcodes (machine instructions) — unreadable without disassembly

**What to write in your report:**
- The output of `xxd firmware.bin | head`
- The file size of `firmware.bin`
- Whether you found the string `"version A"` in the binary
- Interpretation: compiled code ≠ source code, but string literals can leak information

---

### Manipulation 4 — Comparison Before/After (~30 min)

**Goal**: Demonstrate that even a small change in source code produces a different firmware binary.

#### Step 4.1 — Modify the Sketch (Version B)

Change **only** the message string in the sketch:

```cpp
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("TP Firmware UART - version B");  // Changed A → B
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}
```

1. Upload this modified sketch to the Arduino.
2. Verify in Serial Monitor that it now says "version B".
3. **Close the Serial Monitor**.

#### Step 4.2 — Read Flash Again

```bash
avrdude -p m328p -c arduino -P /dev/ttyACM0 -b 115200 -U flash:r:firmware_B.hex:i
```

#### Step 4.3 — Convert Version B

```bash
avr-objcopy -I ihex -O binary firmware_B.hex firmware_B.bin
```

#### Step 4.4 — Compare the Two Versions

```bash
# Binary comparison (will report the first differing byte)
cmp firmware.bin firmware_B.bin

# SHA-256 hash comparison
sha256sum firmware.bin firmware_B.bin

# Detailed diff (optional, shows all differing bytes)
diff <(xxd firmware.bin) <(xxd firmware_B.bin) | head -30
```

On **Windows PowerShell**:
```powershell
Get-FileHash firmware.bin -Algorithm SHA256
Get-FileHash firmware_B.bin -Algorithm SHA256
```

**What to observe:**
- The SHA-256 hashes **must differ** — even a single-character change produces completely different hashes
- `cmp` will show the offset of the first difference
- The `diff` of hex dumps will show exactly which bytes changed

**What to write in your report:**
- Both SHA-256 hashes
- The output of `cmp`
- Interpretation: firmware integrity can be verified via hashing; any modification is detectable

---

## 📊 Observations Table (Fill During Lab)

| Step | Observation | Proof / File | Security Interpretation |
|------|-------------|-------------|------------------------|
| UART (Manip 1) | Serial Monitor shows "TP Firmware UART - version A" | Screenshot of Serial Monitor | UART reveals only what the application sends; not the full firmware |
| Flash Read A (Manip 2) | avrdude successfully reads 32KB Flash | `firmware.hex` (size: ___) | Bootloader allows full Flash read — attack surface if accessible |
| Binary Conversion (Manip 3) | HEX converted to raw binary; strings visible | `firmware.bin` (size: ___) | Sensitive strings (keys, passwords) could be extracted |
| Flash Read B (Manip 4) | Second read after code change | `firmware_B.hex` (size: ___) | Same process works for any firmware version |
| Comparison (Manip 4) | Different SHA-256 hashes | Hash values | Integrity verification is possible; tampering is detectable |

---

## 🔐 Phase 4 — Security Analysis (~30 min)

### Questions to Answer

#### Q1: Why doesn't a UART port automatically allow firmware reading?
UART is just a transport layer (serial communication). It transmits bytes between two endpoints. To read firmware, you need a **software component** (like a bootloader or debug agent) on the MCU that understands read commands and responds with Flash contents. Without such software, UART only carries whatever the application sends.

#### Q2: What software component makes reading possible in this lab?
The **bootloader** (Optiboot on Arduino Uno). It implements the STK500 protocol over UART, allowing avrdude to send read/write commands to the Flash memory.

#### Q3: What is the main asset exposed?
The **firmware** (intellectual property): the compiled application code, including embedded strings, algorithms, cryptographic keys, and any hardcoded credentials.

#### Q4: What risks arise if a programming interface remains accessible on a final product?
- **Firmware extraction** → reverse engineering, IP theft
- **Firmware replacement** → malicious code injection
- **Credential extraction** → hardcoded passwords, API keys, crypto keys
- **Cloning** → counterfeit products
- **Downgrade attacks** → flashing older, vulnerable firmware versions

#### Q5: Does firmware reading compromise confidentiality, integrity, availability, or multiple?
- **Confidentiality**: YES — firmware content (algorithms, secrets) is exposed
- **Integrity**: POTENTIALLY — if the interface also allows writing, an attacker could modify the firmware
- **Availability**: POTENTIALLY — if the interface allows erasing or bricking the device

#### Q6: Why isn't a binary firmware equivalent to the original source code?
Compilation is a **lossy transformation**: variable names, comments, code structure, and high-level abstractions are lost. The binary contains machine opcodes optimized for the target architecture. While disassembly and decompilation can partially reconstruct logic, the original source code cannot be perfectly recovered.

#### Q7: What sensitive information could be found in a poorly designed firmware?
- Hardcoded passwords and API keys
- Private cryptographic keys
- Network credentials (Wi-Fi SSID/passwords)
- Server URLs and endpoints
- Debug messages revealing internal logic
- Encryption algorithms and their weaknesses

#### Q8: Why distinguish UART, bootloader, JTAG/SWD, and ISP programmer?
They are **different layers/interfaces**:
- **UART**: Physical transport layer (serial communication)
- **Bootloader**: Software running on the MCU that uses UART for programming
- **JTAG/SWD**: Hardware debug interfaces that provide direct access to CPU, memory, and registers
- **ISP (In-System Programming)**: Hardware interface (SPI-based) for direct Flash programming, bypassing the bootloader

Each has different capabilities, attack surfaces, and countermeasures.

### Counter-Measures Summary

| Measure | Objective |
|---------|-----------|
| **Attack surface reduction** | Disable unused diagnostic/programming interfaces in production |
| **Secure bootloader** | Restrict read/write functions; add authentication if platform supports it |
| **Secure Boot** | Cryptographically verify firmware authenticity before execution |
| **Signed firmware** | Prevent installation of unauthorized firmware images |
| **Secret protection** | Never store private keys or passwords in plaintext in firmware |
| **Physical protection** | Limit access to test points, connectors, and exposed pins |
| **Logging** | Trace maintenance and update operations when possible |
| **Secure updates** | Authenticate updates and implement anti-rollback protection |

---

## 📝 Report Structure (What to Submit)

Your final report should contain:

1. **Architecture description**: Diagram and explanation of PC → USB-Serial → Bootloader → Flash chain
2. **Commands used**: Every command with the exact parameters adapted to your workstation
3. **Read results**: Screenshot or transcript of avrdude output
4. **Sizes and hashes**: File sizes and SHA-256 of both firmware versions (A and B)
5. **Security analysis**: Argued answers to all 8 questions from Phase 4
6. **Conclusion**: 10–15 lines on the risks of an accessible programming interface

### Grading (Indicative, /20)

| Criterion | Points |
|-----------|--------|
| Preparation and interface identification | 3 |
| Correct Flash reading | 4 |
| Conversion and comparison | 4 |
| Security analysis | 5 |
| Counter-measures and conclusion | 3 |
| Report presentation | 1 |
| **Total** | **20** |

---

## ⏱️ Time Allocation Summary

| Phase | Duration | Description |
|-------|----------|-------------|
| Phase 1 | ~20 min | Theory: understand UART, bootloader, Flash |
| Phase 2 | ~20 min | Setup: connect Arduino, upload sketch, verify serial |
| Phase 3 | ~1h 30min | Hands-on: 4 manipulations (observe, read, convert, compare) |
| Phase 4 | ~30 min | Security analysis: answer questions, write counter-measures |
| Report writing | Remaining | Compile observations, screenshots, and analysis |

---

> [!CAUTION]
> Only perform this lab on a board you **own** or have **explicit authorization** to use. This lab does NOT cover bypassing read protections or security mechanisms.
