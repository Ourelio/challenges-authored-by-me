# Challenges authored by wavess

CTF challenges I wrote and ran, collected from the competitions they were
built for. Mostly DFIR - digital forensics and incident response: working out
what happened on a machine after something went wrong - with one reverse
engineering challenge in the set.

Each folder holds the challenge as players saw it: the brief, whatever files
came with it, and the flag. Point values are left out on purpose; they were
specific to each event's scoreboard and say nothing about the challenge.

> **These are real malware samples.** Several challenges hand you live,
> functional malware. Open them only inside an isolated virtual machine with
> no network path to anything you care about. The archives are password
> protected precisely so nothing detonates by accident.

## The challenges

| Event | Challenge | Category | Difficulty |
|---|---|---|---|
| PETIR Regen 2026 - Qualification | [pemanasan](petir-regen-2026-qual/pemanasan/) | Forensic | baby |
| PETIR Regen 2026 - Qualification | [lagi dengerin lagu apa mas?](petir-regen-2026-qual/lagi-dengerin-lagu-apa-mas/) | Forensic | medium |
| PETIR Regen 2026 - Qualification | [bitcoinnya pepeng dicuri](petir-regen-2026-qual/bitcoinnya-pepeng-dicuri/) | Forensic | hard |
| PETIR Regen 2026 - Qualification | [kena sudah wakoor rnd kita](petir-regen-2026-qual/kena-sudah-wakoor-rnd-kita/) | Forensic | hard |
| PETIR Regen 2026 - Qualification | [main wordle](petir-regen-2026-qual/main-wordle/) | Reverse Engineering | medium |
| National Cyber Week 2025 - Qualification | [Malware Magang](ncw-2025-qual/malware-magang/) | Forensic | hard |
| National Cyber Week 2025 - Final | [brian lagi](ncw-2025-final/brian-lagi/) | Forensic | medium |
| BeeFest 2026 - Qualification | [sudah lama](beefest-2026-qual/sudah-lama/) | Digital Forensic | Medium |
| IFEST CTF 2026 - Qualification | [gratisan mulu sih](ifest-2026-qual/gratisan-mulu-sih/) | Forensic | Hard |
| TechFest HIMTI 2026 | [Basic](techfest-2026/basic/) | Digital Forensic | Hard |
| TechFest HIMTI 2026 - Final | [capek malware mulu](techfest-2026-final/capek-malware-mulu/) | Forensics | Hard |

## Layout

```
<event>/<challenge>/
  README.md   the brief players got, plus the flag
  dist/       files handed to players, where the challenge shipped any
  src/        the server side, for challenges that ran one
```

Challenges with no `dist/` distributed their files over an external link,
which is in that challenge's README along with the archive password.

## Writeups

Each README has a **What this challenge teaches** section that isn't filled
in yet. They're coming.

---

Owen Ourelio Bong - [github.com/Ourelio](https://github.com/Ourelio)
