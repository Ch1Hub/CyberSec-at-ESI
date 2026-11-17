"""Real screenshots for the lab reports.

Terminal windows run in xterm on a private Xvfb display; Wireshark windows
run on the same display.  Nothing is drawn on the user's desktop.
"""
from __future__ import annotations

import hashlib
import os
import shlex
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "screenshots"
SCRIPTS = Path("/tmp/opencode/shots/scripts")
DISPLAY = ":99"
ENV = {**os.environ, "DISPLAY": DISPLAY}

SHOTS.mkdir(exist_ok=True)
SCRIPTS.mkdir(parents=True, exist_ok=True)


def run(cmd, **kwargs):
    return subprocess.run(cmd, shell=isinstance(cmd, str), env=ENV,
                          capture_output=True, text=True, **kwargs)


def windows(title: str) -> list[str]:
    out = run(["xdotool", "search", "--name", f"^{title}$"]).stdout.split()
    return out


def wait_window(title: str, timeout: float = 10) -> str:
    end = time.time() + timeout
    while time.time() < end:
        ids = windows(title)
        if ids:
            return ids[0]
        time.sleep(0.2)
    raise RuntimeError(f"window not found: {title}")


def capture(win: str, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["import", "-window", win, str(out)])
    return out


def trim(path: Path) -> Path:
    from PIL import Image, ImageChops
    im = Image.open(path).convert("RGB")
    bg = im.getpixel((im.width - 4, im.height - 4))
    diff = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L")
    mask = diff.point(lambda v: 255 if v > 14 else 0)
    box = mask.getbbox()
    if box:
        im.crop((0, 0, min(im.width, box[2] + 14), min(im.height, box[3] + 12))).save(path)
    return path


def capture_stable(win: str, out: Path, timeout: float = 20) -> Path:
    """Wait until two consecutive captures are identical, then save."""
    last = b""
    end = time.time() + timeout
    while time.time() < end:
        tmp = out.with_suffix(".tmp.png")
        capture(win, tmp)
        data = tmp.read_bytes()
        if data == last:
            tmp.replace(out)
            return out
        last = data
        time.sleep(0.7)
    raise RuntimeError(f"screen did not settle: {out.name}")


def kill_window(win: str) -> None:
    pid = run(["xdotool", "getwindowpid", win]).stdout.strip()
    if pid:
        run(["kill", pid])
    else:
        run(["xdotool", "windowkill", win])


PROMPT = r"""printf '\033[1;32mchihab@iotlab\033[0m:\033[1;34m%s\033[0m$ ' "$SHORT"
"""


def term(name: str, title: str, workdir: str, cmds: list[str], *,
         short: str | None = None, cols: int = 96, rows: int = 26,
         font: int = 17, timeout: float = 25, settle: float = 2.5) -> Path:
    """Run real commands in a fresh terminal window and screenshot it."""
    workdir = str(Path(workdir).expanduser())
    short = short or workdir.replace(str(Path.home()), "~")
    script = SCRIPTS / f"{name}.sh"
    body = [
        "#!/bin/bash",
        f"cd {shlex.quote(workdir)}",
        "clear",
        "SHORT=" + shlex.quote(short),
        r"""p() { printf '\033[1;32mchihab@iotlab\033[0m:\033[1;34m%s\033[0m$ ' "$SHORT"; }""",
        "run() {",
        "  local cmd=\"$1\" line first=1",
        "  while IFS= read -r line; do",
        "    if [ $first -eq 1 ]; then p; else printf '> '; fi",
        "    printf '%s\\n' \"$line\"; first=0",
        "  done <<< \"$cmd\"",
        "  eval \"$cmd\"",
        "}",
    ]
    for c in cmds:
        body.append(f"run {shlex.quote(c)}")
    body.append("sleep 600")
    script.write_text("\n".join(body) + "\n")
    script.chmod(0o755)

    title_q = shlex.quote(title)
    cmd = (f"xterm -title {title_q} -fa 'Liberation Mono' -fs {font} "
           f"-geometry {cols}x{rows}+0+0 -bg '#101418' -fg '#e6edf3' "
           f"-xrm 'XTerm*scrollBar:false' -e bash {shlex.quote(str(script))} "
           f">/tmp/opencode/shots/xterm.log 2>&1 &")
    subprocess.run(["bash", "-c", cmd], env=ENV, check=False)
    win = wait_window(title, timeout=12)
    time.sleep(settle)
    out = SHOTS / f"{name}.png"
    capture(win, out)
    trim(out)
    kill_window(win)
    time.sleep(0.3)
    return out


# ------------------------------------------------------------------ Wireshark

def wkill() -> None:
    subprocess.run(["pkill", "-x", "wireshark"], capture_output=True)
    time.sleep(1.0)


def ws_open(pcap: str, display_filter: str, *, width=1500, height=900) -> str:
    wkill()
    log = open("/tmp/opencode/shots/wireshark.log", "w")
    subprocess.Popen(
        ["wireshark", "-r", str(pcap), "-Y", display_filter],
        env={**ENV, "QT_QPA_PLATFORM": "xcb"},
        stdout=log, stderr=log,
    )
    title = Path(pcap).name
    win = wait_window(title, timeout=15)
    time.sleep(2.5)
    run(["xdotool", "windowsize", win, str(width), str(height)])
    run(["xdotool", "windowmove", win, "0", "0"])
    time.sleep(1.2)
    return win


def drag(win: str, x1: int, y1: int, x2: int, y2: int) -> None:
    run(["xdotool", "mousemove", "--window", win, str(x1), str(y1)])
    time.sleep(0.2)
    run(["xdotool", "mousedown", "1"])
    time.sleep(0.2)
    run(["xdotool", "mousemove", "--window", win, str(x2), str(y2)])
    time.sleep(0.35)
    run(["xdotool", "mouseup", "1"])
    time.sleep(0.5)


def click(win: str, x: int, y: int) -> None:
    run(["xdotool", "mousemove", "--window", win, str(x), str(y), "click", "1"])
    time.sleep(0.4)


def key(win: str, *keys: str) -> None:
    run(["xdotool", "windowfocus", win])
    for k in keys:
        run(["xdotool", "key", k])
        time.sleep(0.25)


def scroll(win: str, x: int, y: int, n: int, up: bool = False) -> None:
    run(["xdotool", "mousemove", "--window", win, str(x), str(y)])
    button = "4" if up else "5"
    for _ in range(n):
        run(["xdotool", "click", button])
        time.sleep(0.05)
    time.sleep(0.5)


def ws_layout(win: str, *, list_bottom: int = 400) -> None:
    """Resize the panes: short packet list, tall details, narrow bytes pane.

    Must be called on a freshly opened window and before any click, because
    the splitter handles move with the panes.
    """
    drag(win, 300, 694, 300, list_bottom)   # packet list / details splitter
    drag(win, 750, 600, 1150, 600)          # details / bytes splitter
    time.sleep(0.6)


def ws_prep(win: str, *, list_bottom: int = 466, zoom: int = 2) -> None:
    """Lay out the panes, enlarge the font and widen the Info column."""
    ws_layout(win, list_bottom=list_bottom)
    run(["xdotool", "windowfocus", win])
    time.sleep(0.3)
    for _ in range(zoom):
        run(["xdotool", "key", "ctrl+equal"])
        time.sleep(0.25)
    time.sleep(0.6)
    run(["xdotool", "mousemove", "--window", win, "1046", "115"])
    time.sleep(0.25)
    run(["xdotool", "mousedown", "1"])
    time.sleep(0.25)
    run(["xdotool", "mousemove", "--window", win, "880", "115"])
    time.sleep(0.35)
    run(["xdotool", "mouseup", "1"])
    time.sleep(0.8)


def ws_shot(win: str, name: str, *actions) -> Path:
    for a in actions:
        kind = a[0]
        if kind == "click":
            click(win, a[1], a[2])
        elif kind == "key":
            key(win, *a[1:])
        elif kind == "scroll":
            scroll(win, a[1], a[2], a[3], up=(len(a) > 4 and a[4] == "up"))
        elif kind == "drag":
            drag(win, *a[1:])
        elif kind == "wait":
            time.sleep(a[1])
    out = SHOTS / f"{name}.png"
    capture_stable(win, out, timeout=15)
    return out
