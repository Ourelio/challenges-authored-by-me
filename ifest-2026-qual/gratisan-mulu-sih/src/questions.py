#!/usr/bin/env python3
import os
import re
import sys
import threading

BANNER = r"""
  ____  ____      _     _____  ___  ____      _     _   _ 
 / ___||  _ \    / \   |_   _||_ _|/ ___|    / \   | \ | |
| |  _ | |_) |  / _ \    | |   | | \___ \   / _ \  |  \| |
| |_| ||  _ <  / ___ \   | |   | |  ___) | / ___ \ | |\  |
 \____||_| \_\/_/   \_\  |_|  |___||____/ /_/   \_\|_| \_|
 __  __  _   _  _      _   _     ____   ___  _   _ 
|  \/  || | | || |    | | | |   / ___| |_ _|| | | |
| |\/| || | | || |    | | | |   \___ \  | | | |_| |
| |  | || |_| || |___ | |_| |    ___) | | | | | | |
|_|  |_| \___/ |_____| \___/    |____/ |___||_| |_|
"""

FLAG = os.environ.get("FLAG")
if FLAG is None:
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag.txt")) as f:
            FLAG = f.read().strip()
    except OSError:
        FLAG = "IFEST26{fake_flag_for_local_testing}"

TIMEOUT = 30  # seconds per question


# ---------------------------------------------------------------- normalizers
def norm(s):
    """lowercase, trim, collapse inner whitespace"""
    return re.sub(r"\s+", " ", s.strip()).lower()


def norm_path(s):
    """registry / filesystem path: normalize separators, drop trailing slashes,
    accept both HKCU and HKEY_CURRENT_USER style hive names"""
    s = norm(s).replace("/", "\\")
    s = re.sub(r"\\+", "\\\\", s).rstrip("\\")
    s = s.replace("hkey_current_user", "hkcu")
    s = s.replace("hkey_local_machine", "hklm")
    s = s.replace("hkey_classes_root", "hkcr")
    return s


def norm_hex(s):
    """hex value, with or without 0x, with or without leading zeros"""
    s = norm(s).replace(" ", "")
    if s.startswith("0x"):
        s = s[2:]
    return s.lstrip("0") or "0"


def norm_rawhex(s):
    """raw hex string (key material): strip 0x and any separators, keep length"""
    s = norm(s)
    if s.startswith("0x"):
        s = s[2:]
    return re.sub(r"[^0-9a-f]", "", s)


def norm_int(s):
    s = norm(s).replace(",", "").replace("_", "")
    return str(int(s)) if re.fullmatch(r"-?\d+", s) else s


def norm_cmd(s):
    """powershell command: whitespace-insensitive, quote-insensitive"""
    s = norm(s).replace('"', "").replace("'", "")
    s = s.replace(" |", "|").replace("| ", "|")
    s = s.replace(" ,", ",").replace(", ", ",")
    return s


def norm_names(s):
    """underscore separated file list, tolerate spaces around the separators"""
    parts = [p.strip() for p in norm(s).split("_")]
    return "_".join(p for p in parts if p)


# ------------------------------------------------------------------ questions
QUESTIONS = [
    {
        "q": "Which messaging platform did the victim use that delivered the initial malware? (Format: Google)",
        "n": norm,
        "a": ["signal"],
    },
    {
        "q": "What secret word did the threat actor send to the victim? (Format: SecretWord)",
        "n": norm,
        "a": ["bambaustichebat"],
    },
    {
        "q": "What is the first malicious file SHA256 hash? (Format: sha256 hash)",
        "n": norm_rawhex,
        "a": ["d8a9db6fc10aac0aad910b5ea89ff1e85f662662e0d0107582d38f7354ed4b85"],
    },
    {
        "q": "When was the initial malicious file executed? (Format: UTC, hh:mm:ss)",
        "n": norm,
        "a": ["12:43:21"],
    },
    {
        "q": "What is the full path of the registry key the malware created to achieve persistence? "
             "(Format: HKCU\\Microsoft\\Hai|Wavess)",
        "n": norm_path,
        "a": [
            "hkcu\\software\\classes\\clsid\\{645ff040-5081-101b-9f08-00aa002f954e}\\shell\\open\\command",
        ],
    },
    {
        "q": "What file did the initial malware drop onto the system? (Format: filename.ext)",
        "n": norm,
        "a": ["sptfy_update.exe"],
    },
    {
        "q": "What is the full file path of the second malicious file? (Format: C:\\Users\\Paimian\\Downloads\\...)",
        "n": norm_path,
        "a": ["c:\\users\\paimian\\appdata\\local\\temp\\sptfy_update.exe"],
    },
    {
        "q": "What is the IP address of the Command and Control (C2) server? (Format: IP)",
        "n": norm,
        "a": ["192.168.56.1"],
        "reward": (
            "[*] Here's a new file for you to continue your investigaation:\n"
            "    https://binusianorg-my.sharepoint.com/personal/owen_bong_binus_ac_id/"
            "_layouts/15/guestaccess.aspx?share=IQArO5Fq6AgYTZhfzjpGodH4Ad6GPMQvSBn1ePSvDre8YYE&e=tTRiCg"
        ),
    },
    {
        "q": "What keyword triggers the malware to execute data exfiltration? (Format: SecretWord)",
        "n": norm,
        "a": ["spx-exec"],
    },
    {
        "q": "What is the full command sent by the malware to discover files? (Format: command)",
        "n": norm_cmd,
        "a": [
            "get-childitem $env:userprofile\\documents -recurse|select-object fullname,length",
        ],
    },
    {
        "q": "The malware splits its encryption key material into several fragments in memory. "
             "How many fragments are there? (Format: number)",
        "n": norm_int,
        "a": ["8"],
    },
    {
        "q": "Each fragment holds some real key material followed by random padding. "
             "How many bytes of real key material does each fragment hold? (Format: number)",
        "n": norm_int,
        "a": ["34"],
    },
    {
        "q": "Each fragment's allocation is larger than the previous one by a fixed amount. "
             "What is that amount, in bytes? (Format: number)",
        "n": norm_int,
        "a": ["256"],
    },
    {
        "q": "What is the full virtual address at which the third fragment's key material begins? "
             "(Format: hex, e.g. 0x00024373...)",
        "n": norm_hex,
        "a": ["19e0ccd1020"],
    },
    {
        "q": "What is the final 16-byte key used to decrypt the exfiltrated data? "
             "(Format: lowercase hex, no 0x, no separators, e.g. a73bd30dc...)",
        "n": norm_rawhex,
        "a": ["d9d7e8eba15a13fc8a2aa5993adda431"],
    },
    {
        "q": "List the names of all files that were exfiltrated, in the order they appear in the exfil container.\n"
             "   Give each name exactly as stored, including spaces, parentheses, and extension.\n"
             "   (Format: filename1_filename2_filename3, e.g. Annual Report.pdf_photo 2 (2).jpg_main.c)",
        "n": norm_names,
        "a": ["final revision.pdf_slide 1 11 (1).png_untitled2.cpp"],
    },
    {
        "q": "What was the content of the exfiltrated PDF file? (Format: word)",
        "n": norm,
        "a": ["you_solved_the_challenge_so_go_on_submit_this"],
    },
]


# ---------------------------------------------------------------------- io
def say(*args):
    print(*args, flush=True)


def ask(prompt, timeout=TIMEOUT):
    result = []

    def reader():
        say(prompt)
        print("Answer: ", end="", flush=True)
        line = sys.stdin.readline()
        if line:
            result.append(line.strip())

    t = threading.Thread(target=reader)
    t.daemon = True
    t.start()
    t.join(timeout)

    if not result:
        # idle too long -> drop the connection without a word
        sys.exit(0)
    return result[0]


def main():
    say("=" * 62)
    say("\033[91m" + BANNER + "\033[0m")
    say("\033[96m[+] DIFFICULTY : HARD")
    say("[+] AUTHOR     : wavess\033[0m")
    say("=" * 62)
    say("")
    say("[*] Answer every question correctly to get the flag.\n")

    for i, item in enumerate(QUESTIONS, 1):
        given = ask("%2d. %s" % (i, item["q"]))
        if item["n"](given) in item["a"]:
            say("\033[92m[+] Correct!\033[0m")
            if item.get("reward"):
                say("\033[96m%s\033[0m" % item["reward"])
            say("")
        else:
            say("\033[91m[-] Incorrect.\033[0m")
            sys.exit(0)

    say("\n[+] All %d answers correct. Incident reconstructed." % len(QUESTIONS))
    say("[+] Here's your flag: %s" % FLAG)


if __name__ == "__main__":
    main()
