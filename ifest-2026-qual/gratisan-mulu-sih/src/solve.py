#!/usr/bin/env python3
"""Solver: feeds the 18 answers to the question server and prints the flag."""
import sys
from pwn import remote  # pip install pwntools

HOST = "144.91.64.93"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 13337

ANSWERS = [
    "Signal",
    "BambausticHebat",
    "d8a9db6fc10aac0aad910b5ea89ff1e85f662662e0d0107582d38f7354ed4b85",
    "12:43:21",
    r"HKEY_CURRENT_USER\Software\Classes\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\shell\open\command\\",
    "sptfy_update.exe",
    r"C:\Users\Paimian\AppData\Local\Temp\sptfy_update.exe",
    "192.168.56.1",
    "SPX-EXEC",
    r"Get-ChildItem $env:USERPROFILE\Documents -Recurse | Select-Object FullName, Length",
    "8",
    "34",
    "256",
    "0x0000019e0ccd1020",
    "d9d7e8eba15a13fc8a2aa5993adda431",
    "Final Revision.pdf_SLIDE 1 11 (1).png_Untitled2.cpp",
    "you_solved_the_challenge_so_go_on_submit_this",
]

io = remote(HOST, PORT)
for ans in ANSWERS:
    question = io.recvuntil(b"Answer: ").decode(errors="replace")
    print(question, end="")
    print(ans)
    io.sendline(ans.encode())

print(io.recvall(timeout=5).decode(errors="replace"))
