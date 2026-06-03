#!/usr/bin/env python3
"""Generate terminal-styled PDF reports for all 3 labs using fpdf2."""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os, sys, subprocess

# ---------------------------------------------------------------
FONT_SANS_REG = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"
FONT_SANS_ITALIC = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Italic.ttf"
FONT_MONO_REG = "/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf"

# Fallback search if paths differ
for base in ["/usr/share/fonts", "/usr/local/share/fonts", "/home/chihab/.local/share/fonts"]:
    if not os.path.exists(FONT_SANS_REG):
        for root, dirs, files in os.walk(base):
            for f in files:
                if f.lower() == "liberationsans-regular.ttf":
                    FONT_SANS_REG = os.path.join(root, f)
                if f.lower() == "liberationsans-bold.ttf":
                    FONT_SANS_BOLD = os.path.join(root, f)
                if f.lower() == "liberationsans-italic.ttf":
                    FONT_SANS_ITALIC = os.path.join(root, f)
                if f.lower() == "liberationmono-regular.ttf":
                    FONT_MONO_REG = os.path.join(root, f)

# ---------------------------------------------------------------
class TerminalPDF(FPDF):
    def __init__(self, nerd_font_path=None):
        super().__init__(unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)

        # Add unicode fonts
        self.add_font("Sans", "", FONT_SANS_REG, uni=True)
        self.add_font("Sans", "B", FONT_SANS_BOLD, uni=True)
        self.add_font("Sans", "I", FONT_SANS_ITALIC, uni=True)
        self.add_font("Mono", "", FONT_MONO_REG, uni=True)

        self.nerd_font_path = nerd_font_path
        if nerd_font_path and os.path.exists(nerd_font_path):
            self.add_font("NerdMono", "", nerd_font_path, uni=True)
            self.terminal_font = "NerdMono"
        else:
            self.terminal_font = "Mono"

    def header(self):
        self.set_font("Sans", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Ecole Superieure en Informatique, Sidi Bel Abbes  --  Wireless and Mobile Network Security  --  Cys 2SC",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(180, 180, 180)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Sans", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_terminal_block(self, text_lines, title=None):
        margin_x = 15
        max_w = 180
        line_h = 3.8
        pad = 4
        font_sz = 7.5

        lines = text_lines.split("\n")
        block_h = pad * 2 + len(lines) * line_h

        if self.get_y() + block_h > 277:
            self.add_page()

        # Dark background
        self.set_fill_color(18, 18, 18)
        self.rect(margin_x, self.get_y(), max_w, block_h, style="F")

        # Title bar
        if title:
            self.set_fill_color(35, 35, 35)
            th = 5.5
            self.rect(margin_x, self.get_y(), max_w, th, style="F")
            self.set_xy(margin_x + pad, self.get_y() + 1)
            self.set_font("Sans", "B", 7)
            self.set_text_color(180, 180, 180)
            self.cell(0, 4, title)
            self.ln(th)
        else:
            self.ln(pad)

        x_start = margin_x + pad
        self.set_font(self.terminal_font, "", font_sz)

        for raw in lines:
            # Replace unsupported unicode symbols with text equivalents
            raw = raw.replace("✔", "[OK]").replace("✘", "[FAIL]").replace("⚠", "[!]")
            self.set_xy(x_start, self.get_y())
            self._render_terminal_line(raw)
            self.ln(line_h)

        self.ln(pad)

    def _render_terminal_line(self, raw):
        # Default light gray
        self.set_text_color(220, 220, 220)
        stripped = raw.strip()

        if stripped.startswith("╭") or stripped.startswith("╰"):
            self.set_text_color(120, 200, 255)  # cyan prompt
        elif stripped.startswith("✔"):
            self.set_text_color(80, 220, 120)  # green
        elif stripped.startswith("✘") or stripped.startswith("⚠"):
            self.set_text_color(255, 180, 80)  # orange
        elif raw.startswith("  ") and any(c in raw for c in ["→", "•", "-"]):
            self.set_text_color(180, 180, 180)
        elif "─" * 5 in raw:
            self.set_text_color(120, 120, 120)

        self.cell(0, 4, raw)


def find_nerd_font():
    candidates = [
        "/usr/share/fonts/FiraCode/FiraCodeNerdFontMono-Regular.ttf",
        "/usr/share/fonts/FiraCodeNerdFontMono-Regular.ttf",
        "/usr/share/fonts/truetype/FiraCodeNerdFontMono-Regular.ttf",
        "/usr/share/fonts/nerd-fonts/FiraCodeNerdFontMono-Regular.ttf",
        "/usr/share/fonts/nerd-fonts/FiraCode/FiraCodeNerdFontMono-Regular.ttf",
        "/usr/share/fonts/TTF/FiraCodeNerdFontMono-Regular.ttf",
        "/usr/share/fonts/nerd-fonts/Fira Code/FiraCodeNerdFontMono-Regular.ttf",
        "/home/chihab/.local/share/fonts/FiraCodeNerdFontMono-Regular.ttf",
        "/home/chihab/.fonts/FiraCodeNerdFontMono-Regular.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    result = subprocess.run(["fc-list", ":file", "family"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "FiraCode" in line and "Mono" in line and ".ttf" in line:
            path = line.split(":")[0].strip()
            if os.path.exists(path):
                return path
    return None


def build_lab_pdf(lab_num, title, out_path, terminal_text):
    font = find_nerd_font()
    pdf = TerminalPDF(nerd_font_path=font)
    pdf.add_page()

    # Title
    pdf.set_font("Sans", "B", 18)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, f"Lab {lab_num}: {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Sans", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Youcef Chihab Eddine Chikhaoui", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(0, 6, "Wireless and Mobile Network Security -- Cys 2SC", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)

    # Description
    pdf.set_font("Sans", "", 10)
    pdf.set_text_color(50, 50, 50)
    desc = (
        "The following pages contain terminal session screenshots showing the "
        "complete command execution and output for this laboratory exercise. "
        "All commands were run on a Kali Linux virtual machine with an "
        "Alfa AWUS036NHA Wi-Fi adapter in monitor mode."
    )
    pdf.multi_cell(0, 6, desc)
    pdf.ln(6)

    # Terminal block
    pdf.add_terminal_block(terminal_text, title=f"Terminal Session -- Lab {lab_num}")

    # Analysis section
    if pdf.get_y() < 230:
        pdf.ln(4)
        pdf.set_font("Sans", "B", 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, "Analysis Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Sans", "", 10)
        pdf.set_text_color(50, 50, 50)

        if lab_num == 1:
            analysis = (
                "The WEP encryption pipeline was successfully reproduced: CRC-32 "
                "ICV computation (MSB and LSB order), RC4 KSA/PRGA keystream generation, "
                "and XOR encryption. The 24-bit IV and static key design make WEP "
                "cryptographically broken."
            )
        elif lab_num == 2:
            analysis = (
                "The WEP attack was attempted on the DJAWEB_B771 network but could "
                "not be completed because only 451 IVs were available -- far below the "
                "~5000 minimum required by PTW/KoreK statistical attacks. The original "
                "lab router is no longer accessible, preventing further IV collection."
            )
        else:
            analysis = (
                "The WPA2-PSK passphrase was recovered via offline dictionary attack "
                "after capturing the 4-way handshake. The PBKDF2-SHA1 key derivation "
                "with only 4096 iterations is weak by modern standards. WPA3-SAE is "
                "recommended to resist offline guessing."
            )
        pdf.multi_cell(0, 6, analysis)

    pdf.output(out_path)
    print(f"  PDF created: {out_path}")


# ---------------------------------------------------------------
def main():
    base = "/home/chihab/Documents/cys2CS/s2/wirelessNet/terminal_reports"
    reports_dir = "/home/chihab/Documents/cys2CS/s2/wirelessNet"

    labs = [
        (1, "WEP Encryption", f"{reports_dir}/Lab1_Terminal_Report.pdf", f"{base}/lab1_output.txt"),
        (2, "WEP Exploitation", f"{reports_dir}/Lab2_Terminal_Report.pdf", f"{base}/lab2_output.txt"),
        (3, "WPA/WPA2 Exploitation", f"{reports_dir}/Lab3_Terminal_Report.pdf", f"{base}/lab3_output.txt"),
    ]

    for num, title, out_path, txt_path in labs:
        if not os.path.exists(txt_path):
            print(f"  Missing text file: {txt_path}")
            continue
        with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        build_lab_pdf(num, title, out_path, text)


if __name__ == "__main__":
    main()
