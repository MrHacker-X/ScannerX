#!/usr/bin/env bash
# ScannerX installer — github.com/MrHacker-X
set -u

# ---------- colors ----------
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    RD=$'\e[1;91m'; GR=$'\e[1;92m'; YL=$'\e[1;93m'; CY=$'\e[1;96m'; WH=$'\e[1;97m'; XX=$'\e[0m'
else
    RD=""; GR=""; YL=""; CY=""; WH=""; XX=""
fi

info() { printf '%s[*]%s %s\n' "$CY" "$XX" "$1"; }
ok()   { printf '%s[+]%s %s\n' "$GR" "$XX" "$1"; }
warn() { printf '%s[!]%s %s\n' "$YL" "$XX" "$1"; }
err()  { printf '%s[x]%s %s\n' "$RD" "$XX" "$1" >&2; }
fail() { err "$1"; exit 1; }

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---------- Termux detection ----------
IS_TERMUX=0
[ -n "${TERMUX_VERSION:-}" ] && IS_TERMUX=1

# ---------- privilege + prefix (Linux) ----------
SUDO=""
BIN_DIR="/usr/local/bin"
APP_DIR="/usr/local/share/ScannerX"
if [ "$IS_TERMUX" -eq 0 ]; then
    if [ "$(id -u)" -eq 0 ]; then
        SUDO=""
    elif command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        warn "No root and no sudo — installing to ~/.local/bin instead."
        BIN_DIR="$HOME/.local/bin"
        APP_DIR="$HOME/.local/share/ScannerX"
        mkdir -p "$BIN_DIR"
    fi
fi

# ---------- uninstall mode ----------
if [ "${1:-}" = "--uninstall" ]; then
    if [ "$IS_TERMUX" -eq 1 ]; then
        rm -rf "$HOME/../usr/share/ScannerX" "$PREFIX/bin/scanx"
        rm -rf "/data/data/com.termux/files/usr/share/ScannerX" "/data/data/com.termux/files/usr/bin/scanx"
    else
        $SUDO rm -rf "$APP_DIR"
        rm -f "$BIN_DIR/scanx"
    fi
    ok "ScannerX removed."
    exit 0
fi

# ---------- banner ----------
printf '%s\n' "${RD}<------[${WH}ScannerX · MrHacker-X${RD}]------>${XX}"
echo

# ---------- dependencies ----------
info "Installing dependencies..."
if [ "$IS_TERMUX" -eq 1 ]; then
    apt update -y || warn "apt update failed, continuing..."
    apt install python3 -y || fail "Could not install python3. Run: apt install python3"
else
    PM=""
    for candidate in apt-get dnf yum pacman zypper; do
        command -v "$candidate" >/dev/null 2>&1 && { PM="$candidate"; break; }
    done
    [ -n "$PM" ] || fail "No supported package manager found (apt-get/dnf/yum/pacman/zypper)."
    case "$PM" in
        apt-get)      $SUDO apt-get update -y && $SUDO apt-get install -y python3 python3-pip wget ;;
        dnf)          $SUDO dnf install -y python3 python3-pip wget ;;
        yum)          $SUDO yum install -y python3 python3-pip wget ;;
        pacman)       $SUDO pacman -Sy --noconfirm python python-pip wget ;;
        zypper)       $SUDO zypper --non-interactive install python3 python3-pip wget ;;
    esac
fi
ok "Dependencies ready."

# ---------- install ----------
info "Installing ScannerX..."
if [ "$IS_TERMUX" -eq 1 ]; then
    APP_DIR="$PREFIX/share/ScannerX"
    BIN_DIR="$PREFIX/bin"
    mkdir -p "$APP_DIR"
    cp "$REPO_DIR/scannerx.py" "$APP_DIR/scannerx.py"
    chmod +x "$APP_DIR/scannerx.py"
    cat > "$BIN_DIR/scanx" <<EOF
#!/data/data/com.termux/files/usr/bin/env bash
exec python3 $APP_DIR/scannerx.py "\$@"
EOF
    chmod +x "$BIN_DIR/scanx"
else
    $SUDO mkdir -p "$APP_DIR"
    $SUDO cp "$REPO_DIR/scannerx.py" "$APP_DIR/scannerx.py"
    $SUDO chmod +x "$APP_DIR/scannerx.py"
    printf '#!/usr/bin/env bash\nexec python3 %s/scannerx.py "$@"\n' "$APP_DIR" > /tmp/scanx-launcher
    $SUDO cp /tmp/scanx-launcher "$BIN_DIR/scanx"
    $SUDO chmod +x "$BIN_DIR/scanx"
    rm -f /tmp/scanx-launcher
fi
ok "Installed to $APP_DIR"
ok "Command: $BIN_DIR/scanx"

# ---------- done ----------
echo
printf '%s\n' "${RD}<==============================================>${XX}"
printf '%s\n' "${GR}  ScannerX installed${XX}"
printf '%s\n' "${WH}  Launch: scanx <domain>${XX}"
printf '%s\n' "${RD}<==============================================>${XX}"
echo
info "Example: ${WH}scanx example.com${XX}"
info "Uninstall: ${WH}bash setup.sh --uninstall${XX}"
echo
