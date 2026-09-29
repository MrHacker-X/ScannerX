<div align="center">

# ⃤ S C A N N E R X ⃤

🔍 **55 OSINT scan targets. 10 categories. One command.**

<img src="https://img.shields.io/github/stars/MrHacker-X/ScannerX?style=for-the-badge&color=orange">
<img src="https://img.shields.io/github/forks/MrHacker-X/ScannerX?color=cyan&style=for-the-badge&color=purple">
<img src="https://img.shields.io/github/watchers/MrHacker-X/ScannerX?color=cyan&style=for-the-badge&color=purple">
<img src="https://img.shields.io/github/issues/MrHacker-X/ScannerX?color=red&style=for-the-badge">
<img src="https://img.shields.io/github/license/MrHacker-X/ScannerX?style=for-the-badge&color=blue"><br>
<img src="https://hits.dwyl.com/MrHacker-X/ScannerX.svg" width="140" height="28"><br><br>
<img src="https://img.shields.io/badge/Author-MrHacker--X-purple?style=flat-square">
<img src="https://img.shields.io/badge/Open%20Source-Yes-cyan?style=flat-square">
<img src="https://img.shields.io/badge/Written%20In-Python-blue?style=flat-square">
<img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-green?style=flat-square">

</div>

---

## 📋 Table of Contents

- [🎯 Why ScannerX?](#-why-scannerx)
- [✨ Features](#-features)
- [🖥️ Preview](#️-preview)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🧩 Usage](#-usage)
- [❓ FAQ](#-faq)
- [🧰 Tech Stack](#-tech-stack)
- [⚠️ Disclaimer](#️-disclaimer)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👤 Developer](#-developer)

---

## 🎯 Why ScannerX?

> OSINT on a domain means juggling dozens of bookmarks -VirusTotal, crt.sh, Shodan, ViewDNS, SSL Labs, dork pages… **ScannerX** keeps them all in one clean menu and launches every target for your domain with one keypress.
>
> Fully transparent Python -no obfuscation, no self-deleting installers, no fake loading bars. Read every line before you run it.

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 🧭 | **10 scan categories** | Subdomain enum, Port/DNS/Whois, Headers, TLS/SSL, Analyze, Wayback, Search engines, Google + GitHub dorks |
| 🌐 | **55 curated targets** | Every URL parameterized with your domain -no hardcoded leftovers |
| 🌊 | **Run All waves** | Fires all 10 categories in sequence with ENTER-gated waves |
| 🧹 | **Cleaned link set** | Dead services (Threatcrowd, old Censys) removed; broken/hardcoded URLs fixed |
| 🖥️ | **Termux + Linux** | Safe opener with `xdg-open` → `termux-open` fallback; URL list printed if no opener exists |
| 🛡️ | **Safe installer** | Package-manager detection (apt/dnf/yum/pacman/zypper), sudo fallback to `~/.local/bin`, no `rm -rf *` |
| 🧯 | **Built-in uninstall** | `scanx` menu or `bash setup.sh --uninstall` -clean removal |
| ⚡ | **Smart input** | Strips `https://`, paths and ports; rejects invalid domains with a clear error |
| ⌨️ | **Typographic UI** | Ruled status header (target · engine · armed), dot-leader menu rows, gold-on-dark monochrome theme — renders cleanly everywhere |
| 📖 | **Transparent** | Plain readable Python -no obfuscation |

---

## 🖥️ Preview

<div align="center">

![ScannerX Menu](https://i.ibb.co/5xJ94H1d/Screenshot-From-2026-09-29-08-56-28.png)

</div>

```bash
$ scanx example.com

  S C A N N E R X
  osint recon launcher · v2.1

  ──────────────────────────────────────────────────────────
  target      example.com
  engine      xdg-open
  armed       10 categories · 55 services
  ──────────────────────────────────────────────────────────

  Main

    1  Show Category  ···· one scan wave
    2  Run All        ···· all waves, gated
    3  Follow         ···· github · socials
    4  About
    5  Uninstall      ···· danger  
    0  Exit

  5 removes the tool · 0 just exits

  ›
```

> No ASCII noise, no fake gauges — a typographic UI that renders cleanly in every terminal. Run it as `scanx <domain>` or straight from source with `python3 scannerx.py <domain>`; menus, help and errors always show the name you actually used.

 
---

## 🚀 Quick Start

```bash
apt update -y && apt upgrade -y
apt install git python3 -y
git clone https://github.com/MrHacker-X/ScannerX.git
cd ScannerX
bash setup.sh
scanx example.com
```

---

## 📦 Installation

### Supported Systems

| System | Supported | Package Manager |
|--------|-----------|-----------------|
| 🤖 **Termux (Android)** | ✅ | `apt` |
| 🐧 **Linux (Debian/Ubuntu)** | ✅ | `apt-get` |
| 🐧 **Fedora/RHEL** | ✅ | `dnf` / `yum` |
| 🐧 **Arch** | ✅ | `pacman` |
| 🐧 **openSUSE** | ✅ | `zypper` |
| 🍎 **macOS** | ❌ | Refused |
| 🪟 **Windows** | ❌ | Refused |

### Steps

1. **Update your system**
    ```bash
    apt update -y && apt upgrade -y        # Termux / Debian
    ```
2. **Install Git and Python**
    ```bash
    apt install git python3 -y
    ```
3. **Clone the repository**
    ```bash
    git clone https://github.com/MrHacker-X/ScannerX.git
    cd ScannerX
    ```
4. **Run the installer**
    ```bash
    bash setup.sh
    ```
5. **Launch**
    ```bash
    scanx example.com
    ```

<details>
<summary><b>🔍 What exactly does the installer do?</b></summary>

- Detects your environment: **Termux** or **Linux**
- On Linux, auto-detects your package manager (`apt-get` / `dnf` / `yum` / `pacman` / `zypper`)
- Installs `python3` if missing
- Copies `scannerx.py` to its share directory and drops a `scanx` launcher into your `$PATH`
- On Linux **without root/sudo**, falls back safely to `~/.local/bin`
- Does **not** delete the repo folder, does **not** use `rm -rf *`, and does **not** obfuscate a single line

</details>

<details>
<summary><b>🧯 Uninstalling</b></summary>

Two ways:

```bash
bash setup.sh --uninstall
```

or pick **`[05] Uninstall It`** inside the tool and confirm with `y`.

</details>

---

## 🧩 Usage

```bash
scanx <domain>
```

| Option | What it does |
|--------|--------------|
| `[01] Show Category` | Pick one of the 10 scan categories |
| `[02] Run All Scan` | Launch every category in ENTER-gated waves |
| `[03] Follow` | Open MrHacker-X's socials |
| `[04] About` | Tool info |
| `[05] Uninstall` | Remove ScannerX completely |
| `[00] Quit` | Exit |

### Scan categories

| Category | Targets | Sample services |
|----------|---------|-----------------|
| Subdomain Enumeration | 11 | VirusTotal, crt.sh, Riddler, SecurityTrails |
| Port, DNS, Whois | 5 | ViewDNS, DNSlytics |
| Header, Built With | 3 | SecurityHeaders, BuiltWith |
| TLS/SSL Certificates | 3 | SSL Labs, certdb, Google CT |
| Analyze | 4 | Netcraft, Sucuri, Mozilla Observatory |
| Wayback Machine | 1 | web.archive.org |
| Search Engines | 4 | Shodan, ZoomEye, FOFA |
| Google Dorks | 10 | site/ext/inurl dorks |
| Github Dorks P1 | 8 | keys, dumps, secrets |
| Github Dorks P2 | 6 | htpasswd, history, API keys |

---

## ❓ FAQ

**Does ScannerX hack anything?**
No. It launches public OSINT/analysis pages in your browser with your target pre-filled. Everything it opens is a service you could visit manually.

**Why do so many tabs open?**
Each category fires its full target list. Use single categories, or close tabs as you go during Run All.

**My browser didn't open -what now?**
ScannerX prints the full URL list to the terminal instead, so nothing is lost.

**Does it work on Windows or macOS?**
No -Linux and Termux only, by design.

**I ran `python3 scannerx.py example.com` and menus still say scanx?**
They don't — ScannerX derives every name it prints (help, errors, menus) from how you invoked it. Command or direct file, it always shows the right one.

**How do I remove it?**
`bash setup.sh --uninstall`, or option `[05]` in the menu.

---

## 🧰 Tech Stack

| | Technology |
|---|-----------|
| 🐍 | **Python 3** -100% of the tool |
| 🧵 | **subprocess / shutil** -safe process & path handling |
| 🤖 | **Termux / Linux** -target platforms |

---

## ⚠️ Disclaimer

> ScannerX is intended **for educational purposes and authorized security testing only**. You are responsible for how you use it -scanning targets you don't have permission to test may be illegal in your jurisdiction. The author is **not responsible** for any misuse or damage caused by this tool.

---

## 🤝 Contributing

Contributions are always welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 👤 Developer

| | |
|---|---|
| 👨‍💻 **Dev** | MrHacker-X |
| 🐙 **GitHub** | [github.com/MrHacker-X](https://github.com/MrHacker-X) |
| 📧 **Email** | [contact@vritrasec.com](mailto:contact@vritrasec.com) |
| 🌐 **Website** | [vritrasec.com](https://vritrasec.com) |
| 🔗 **Network** | [link.vritrasec.com](https://link.vritrasec.com) |

---

<div align="center">

**⭐ Star this repository if ScannerX sharpened your recon! ⭐**

Made with 🔍 by **MrHacker-X**

</div>
