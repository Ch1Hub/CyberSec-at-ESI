#!/usr/bin/env bash
set -euo pipefail

INPUT_SOURCE="${1:-auto}"
SINCE_WINDOW="${2:-10 minutes ago}"
TMP_SOURCE=""
SOURCE_LABEL=""
PARSE_FILE=""

cleanup() {
  if [[ -n "$TMP_SOURCE" && -f "$TMP_SOURCE" ]]; then
    rm -f "$TMP_SOURCE"
  fi
}
trap cleanup EXIT

detect_log_file() {
  local candidate
  for candidate in /var/log/auth.log /var/log/secure; do
    if [[ -f "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

readable_or_sudo_copy() {
  local source_file="$1"

  if [[ -r "$source_file" ]]; then
    PARSE_FILE="$source_file"
    return 0
  fi

  if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    TMP_SOURCE="$(mktemp)"
    sudo cat "$source_file" > "$TMP_SOURCE"
    PARSE_FILE="$TMP_SOURCE"
    return 0
  fi

  echo "Error: cannot read $source_file (run with sudo or pass a readable log file)." >&2
  return 1
}

journal_to_tmp() {
  TMP_SOURCE="$(mktemp)"
  journalctl --since "$SINCE_WINDOW" --no-pager > "$TMP_SOURCE"
  PARSE_FILE="$TMP_SOURCE"
}

prepare_source() {
  local detected_file=""

  if [[ "$INPUT_SOURCE" != "auto" ]]; then
    if [[ ! -f "$INPUT_SOURCE" ]]; then
      echo "Error: log file not found: $INPUT_SOURCE" >&2
      return 1
    fi
    SOURCE_LABEL="$INPUT_SOURCE"
    readable_or_sudo_copy "$INPUT_SOURCE"
    return 0
  fi

  detected_file="$(detect_log_file || true)"
  if [[ -n "$detected_file" ]]; then
    if [[ -r "$detected_file" ]]; then
      SOURCE_LABEL="$detected_file"
      PARSE_FILE="$detected_file"
      return 0
    fi

    if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
      SOURCE_LABEL="$detected_file (via sudo)"
      readable_or_sudo_copy "$detected_file"
      return 0
    fi

    if command -v journalctl >/dev/null 2>&1; then
      SOURCE_LABEL="journalctl --since \"$SINCE_WINDOW\""
      journal_to_tmp
      return 0
    fi

    echo "Error: cannot read $detected_file and journalctl is unavailable." >&2
    return 1
  fi

  if command -v journalctl >/dev/null 2>&1; then
    SOURCE_LABEL="journalctl --since \"$SINCE_WINDOW\""
    journal_to_tmp
    return 0
  fi

  echo "Error: no auth log source available." >&2
  return 1
}

prepare_source

awk -v SOURCE_LABEL="$SOURCE_LABEL" '
BEGIN {
  failed_login = 0
  priv_esc = 0
}
{
  line = $0

  if (line ~ /(sshd|login|gdm-password).*(Failed password|Failed none|authentication failure)/ ||
      line ~ /sshd.*Invalid user/ ||
      line ~ /pam_unix\((sshd|login):auth\): authentication failure/ ||
      line ~ /FAILED LOGIN/) {
    failed_login++
    failed_login_lines[failed_login] = NR ": " line
  }

  if (line ~ /(sudo|su)(\[[0-9]+\])?:/ ||
      line ~ /pam_unix\((sudo|su):auth\)/ ||
      line ~ /session opened for user root/ ||
      line ~ /incorrect password attempts/ ||
      line ~ /NOT in sudoers/) {
    priv_esc++
    priv_esc_lines[priv_esc] = NR ": " line
  }
}
END {
  print "===== Mini HIDS Report ====="
  print "Log source: " SOURCE_LABEL
  print ""
  print "Failed login attempts: " failed_login
  if (failed_login > 0) {
    print "--- Details (failed login) ---"
    for (i = 1; i <= failed_login; i++) {
      print failed_login_lines[i]
    }
    print ""
  }

  print "Privilege escalation attempts: " priv_esc
  if (priv_esc > 0) {
    print "--- Details (privilege escalation) ---"
    for (i = 1; i <= priv_esc; i++) {
      print priv_esc_lines[i]
    }
  }
}
' "$PARSE_FILE"
