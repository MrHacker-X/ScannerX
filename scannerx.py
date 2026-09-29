## ScannerX — github.com/MrHacker-X

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from urllib.parse import urlparse

if os.name != "posix":
    print("ScannerX runs on Linux and Termux only.")
    sys.exit(1)

if sys.stdout.isatty() and os.environ.get("NO_COLOR") is None:
    WH  = "\033[1;97m"      # bold white — labels & values
    YL  = "\033[38;5;179m"  # champagne gold — numbers, rules, prompt
    GR  = "\033[38;5;150m"  # sage — success ticks
    DM  = "\033[38;5;245m"  # dim — hints, keys, dots
    XX  = "\033[0m"
else:
    WH = YL = GR = DM = XX = ""

PROG = os.path.basename(sys.argv[0]) or "scannerx.py"
VERSION = "2.1"
DOMAIN = ""

TOOL = shutil.which("xdg-open") or shutil.which("termux-open-url") or shutil.which("termux-open") or shutil.which("open")

SITES = {
    "Subdomain Enumeration": [
        "https://www.virustotal.com/gui/domain/{d}/relations",
        "https://crt.sh/?q=%25.{d}",
        "https://riddler.io/search?q=pld:{d}",
        "https://riddler.io/search?q=host:{d}",
        "https://riddler.io/search?q=keyword%3A{d}&view_type=data_table",
        "https://findsubdomains.com/subdomains-of/{d}",
        "https://dnstable.com/domain/{d}",
        "https://securitytrails.com/list/apex_domain/{d}",
        "https://certspotter.com/api/v0/certs?domain={d}",
        "https://www.google.ca/search?q=site:*.{d}",
        "https://www.google.ca/search?q=site:*.*.{d}",
    ],
    "Port, DNS, Whois": [
        "https://viewdns.info/portscan/?host={d}",
        "https://viewdns.info/dnsreport/?domain={d}",
        "https://viewdns.info/reversewhois/?q={d}",
        "https://viewdns.info/whois/?domain={d}",
        "https://dnslytics.com/domain/{d}",
    ],
    "Header, Built With": [
        "https://securityheaders.com/?q={d}&followRedirects=on",
        "https://viewdns.info/httpheaders/?domain={d}",
        "https://builtwith.com/{d}",
    ],
    "TLS/SSL Certificates": [
        "https://www.ssllabs.com/ssltest/analyze.html?d={d}",
        "https://certdb.com/search/index?q=domain%3A%22{d}%22",
        "https://transparencyreport.google.com/https/certificates?cert_search=include_expired:true;include_subdomains:true;domain:{d}&lu=cert_search_cert",
    ],
    "Analyze": [
        "https://toolbar.netcraft.com/site_report?url={d}",
        "https://sitecheck.sucuri.net/results/{d}",
        "https://www.siteguarding.com/spam/viewreport?domain={d}",
        "https://observatory.mozilla.org/analyze/{d}",
    ],
    "Wayback Machine": [
        "https://web.archive.org/web/*/{d}",
    ],
    "Search Engines": [
        "https://fofa.so/result?q={d}&full=true",
        "https://www.zoomeye.org/searchResult?q={d}",
        "https://www.zoomeye.org/searchResult/bugs?q={d}",
        "https://www.shodan.io/search?query={d}",
    ],
    "Google Dorks": [
        "https://www.google.ca/search?q=site:{d}+ext:cgi+OR+ext:php+OR+ext:asp+OR+ext:aspx+OR+ext:jsp+OR+ext:jspx+OR+ext:swf+OR+ext:fla+OR+ext:xml",
        "https://www.google.ca/search?q=site:{d}+ext:doc+OR+ext:docx+OR+ext:csv+OR+ext:pdf+OR+ext:txt+OR+ext:log+OR+ext:bak",
        "https://www.google.ca/search?q=site:{d}+ext:action+OR+struts",
        "https://www.google.ca/search?q=site:pastebin.com+{d}",
        "https://www.google.ca/search?q=site:linkedin.com+employees+{d}",
        "https://www.google.ca/search?q=site:{d}+username+OR+password+OR+login+OR+root+OR+admin",
        "https://www.google.ca/search?q=site:{d}+inurl:shell+OR+inurl:backdoor+OR+inurl:wso+OR+inurl:cmd+OR+shadow+OR+passwd+OR+boot.ini+OR+inurl:backdoor",
        "https://www.google.ca/search?q=site:{d}+inurl:readme+OR+inurl:license+OR+inurl:install+OR+inurl:setup+OR+inurl:config",
        "https://www.google.ca/search?q=site:{d}+inurl:wp-+OR+inurl:plugin+OR+inurl:upload+OR+inurl:download",
        "https://www.google.ca/search?q=site:{d}+inurl:redir+OR+inurl:url+OR+inurl:redirect+OR+inurl:return+OR+inurl:src=http+OR+inurl:r=http",
    ],
    "Github Dorks P1": [
        "https://github.com/search?q={d}",
        "https://github.com/search?q={d}+filename:.npmrc_auth",
        "https://github.com/search?q={d}+filename:.dockercfg+auth",
        "https://github.com/search?q={d}+extension:pem+private",
        "https://github.com/search?q={d}+extension:ppk+private",
        "https://github.com/search?q={d}+filename:id_rsa",
        "https://github.com/search?q={d}+filename:id_dsa",
        "https://github.com/search?q={d}+extension:sql+mysql+dump",
    ],
    "Github Dorks P2": [
        "https://github.com/search?q={d}+extension:sql+mysql+dump+password",
        "https://github.com/search?q={d}+filename:.htpasswd",
        "https://github.com/search?q={d}+HEROKU_API_KEY+language:shell",
        "https://github.com/search?q={d}+HEROKU_API_KEY+language:json",
        "https://github.com/search?q={d}+filename:.bash_history",
        "https://github.com/search?q={d}+filename:.history",
    ],
}

# ---------- theme helpers ----------

ANSI = re.compile(r"\033\[[0-9;]*m")

def vlen(s):
    return len(ANSI.sub("", s))

WIDTH = 58

def rule():
    print(f"  {YL}{'─' * WIDTH}{XX}")

def kv(key, value, gap=12):
    print(f"  {DM}{key:<{gap}}{XX}{WH}{value}{XX}")

def wordmark():
    print(f"\n  {WH}S C A N N E R X{XX}")
    print(f"  {DM}osint recon launcher · v{VERSION}{XX}")

def header():
    print()
    wordmark()
    print()
    rule()
    total = sum(len(v) for v in SITES.values())
    kv("target", DOMAIN)
    kv("engine", os.path.basename(TOOL) if TOOL else "none — urls printed")
    kv("armed", f"{len(SITES)} categories · {total} services")
    rule()

def section(title):
    print(f"\n  {WH}{title}{XX}\n")

def item(num, label, desc="", dim=False, align=13):
    label_c = DM if dim else WH
    gap = " " * max(0, align - len(label))
    if desc:
        print(f"  {YL}{num:>3}{XX}  {label_c}{label}{XX}{gap}  {DM}···· {desc}{XX}")
    else:
        print(f"  {YL}{num:>3}{XX}  {label_c}{label}{XX}")

def foot(hint):
    print(f"\n  {DM}{hint}{XX}")

def ask():
    return input(f"\n  {YL}›{XX} ").strip()

def bad_input():
    print(f"  {DM}unknown option — try again{XX}")
    time.sleep(0.6)

def pause(msg=None):
    try:
        input(f"\n  {DM}enter to continue{XX} ")
    except (KeyboardInterrupt, EOFError):
        bye()

def clear():
    os.system("clear")

# ---------- core actions ----------

def open_url(url):
    if TOOL:
        subprocess.Popen([TOOL, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def launch(category):
    urls = [u.format(d=DOMAIN) for u in SITES[category]]
    n = len(urls)
    section(f"{category} — {n} service{'s' if n != 1 else ''}")
    if not TOOL:
        for u in urls:
            print(f"  {DM}·{XX} {WH}{u}{XX}")
        print(f"\n  {YL}[!]{XX} {WH}no browser opener found — urls printed above{XX}")
        return
    for i, u in enumerate(urls, 1):
        open_url(u)
        host = urlparse(u).netloc
        print(f"  {YL}{i:02d}{XX}  {WH}{host}{XX}{' ' * max(1, 30 - len(host))}{GR}✓{XX}")
        time.sleep(0.15)
    print(f"\n  {DM}{n} opened — switch to your browser{XX}")

def run_all():
    total = sum(len(v) for v in SITES.values())
    print(f"\n  {DM}fires all {len(SITES)} waves · ~{total} pages — close tabs as you go{XX}")
    for name in SITES:
        input(f"\n  {DM}enter to launch{XX} {WH}{name}{XX} ")
        launch(name)
    print(f"\n  {GR}✓{XX} {WH}all waves launched{XX}")
    bye()

def follow():
    socials = [
        ("GitHub",    "https://github.com/MrHacker-X"),
        ("Instagram", "https://instagram.com/vritrasec"),
        ("YouTube",   "https://youtube.com/@Technolex"),
    ]
    while True:
        clear(); header()
        section("Follow MrHacker-X")
        for i, (name, _) in enumerate(socials, 1):
            item(f"{i}", name)
        foot("95 back · 0 exit · enter a number to open")
        c = ask()
        if c == "95": return
        if c in ("0", "00"): bye()
        if c.isdigit() and 1 <= int(c) <= len(socials):
            name, url = socials[int(c) - 1]
            open_url(url)
            print(f"  {GR}✓{XX} {WH}{name} opened{XX}")
            time.sleep(0.4)
        elif c:
            bad_input()

def about():
    clear()
    print()
    wordmark()
    print()
    rule()
    kv("author", "MrHacker-X")
    kv("version", VERSION)
    kv("categories", str(len(SITES)))
    kv("services", str(sum(len(v) for v in SITES.values())))
    kv("usage", f"{PROG} <domain>")
    kv("github", "github.com/MrHacker-X")
    rule()
    foot("educational & authorized testing use only")
    pause()

def confirm_uninstall():
    conf = input(f"\n  {DM}really uninstall ScannerX? type{XX} {WH}y{XX} {DM}to confirm{XX} ").strip().lower()
    if conf != "y":
        print(f"  {DM}aborted{XX}")
        return
    final = input(f"  {YL}[!]{XX} {WH}removes the command, files and this folder — sure? [y/N]{XX} ").strip().lower()
    if final != "y":
        print(f"  {DM}aborted{XX}")
        return
    here = os.path.dirname(os.path.abspath(__file__))
    targets = ["/usr/local/bin/scanx", os.path.expanduser("~/.local/bin/scanx"),
               f"{here}/scannerx.py", here]
    for t in targets:
        if t == here and os.path.basename(here) == "ScannerX":
            shutil.rmtree(here, ignore_errors=True)
        elif os.path.lexists(t):
            try:
                os.remove(t)
            except (IsADirectoryError, PermissionError):
                shutil.rmtree(t, ignore_errors=True)
    print(f"\n  {GR}✓{XX} {WH}ScannerX uninstalled{XX}")
    sys.exit(0)

def bye():
    print(f"\n  {DM}scannerx · {WH}github.com/MrHacker-X{DM} · over and out{XX}\n")
    sys.exit(0)

# ---------- menus ----------

def submenu():
    while True:
        clear(); header()
        section("Scan categories")
        keys = list(SITES)
        w = max(len(k) for k in keys)
        for i, name in enumerate(keys, 1):
            item(f"{i}", name, f"{len(SITES[name])} services", align=w)
        foot("95 back · 0 exit")
        c = ask()
        if c == "95": return
        if c in ("0", "00"): bye()
        if c.isdigit() and 1 <= int(c) <= len(keys):
            launch(keys[int(c) - 1])
            pause()
        elif c:
            bad_input()

def menu():
    while True:
        clear(); header()
        section("Main")
        item("1", "Show Category", "one scan wave")
        item("2", "Run All", "all waves, gated")
        item("3", "Follow", "github · socials")
        item("4", "About")
        item("5", "Uninstall", "danger", dim=True)
        item("0", "Exit")
        foot("5 removes the tool · 0 just exits")
        c = ask()
        if c in ("1", "01"): submenu()
        elif c in ("2", "02"): run_all()
        elif c in ("3", "03"): follow()
        elif c in ("4", "04"): about()
        elif c in ("5", "05"): confirm_uninstall()
        elif c in ("0", "00"): bye()
        elif c: bad_input()

# ---------- entry ----------

def main():
    global DOMAIN
    ap = argparse.ArgumentParser(
        prog=PROG,
        description="ScannerX — OSINT recon launcher for domains (github.com/MrHacker-X)",
        epilog=f"Example: {PROG} example.com")
    ap.add_argument("domain", help="target domain, e.g. example.com")
    ap.add_argument("-v", "--version", action="version", version=f"ScannerX {VERSION}")
    args = ap.parse_args()
    DOMAIN = args.domain.strip().lower()
    if DOMAIN.startswith(("http://", "https://")):
        DOMAIN = DOMAIN.split("//", 1)[1]
    DOMAIN = DOMAIN.split("/")[0].split(":")[0]
    if "." not in DOMAIN:
        ap.error(f"invalid domain: {args.domain}")
    try:
        menu()
    except KeyboardInterrupt:
        bye()

if __name__ == "__main__":
    main()
