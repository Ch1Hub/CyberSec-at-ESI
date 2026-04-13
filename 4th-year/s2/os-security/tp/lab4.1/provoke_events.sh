#!/usr/bin/env bash
set -euo pipefail

TARGET_LOG_FILE="${1:-}"
BAD_PASSWORD="${BAD_PASSWORD:-WrongPassword!123}"
START_TIME=""

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

is_ssh_local_reachable() {
  timeout 2 bash -c "cat < /dev/null > /dev/tcp/127.0.0.1/22" >/dev/null 2>&1
}

run_failed_ssh_attempts() {
  local tries=2
  local i

  if ! command -v ssh >/dev/null 2>&1; then
    echo "[WARN] ssh client not found; skipping failed SSH login attempts."
    return 0
  fi

  if ! is_ssh_local_reachable; then
    echo "[WARN] local sshd not reachable on 127.0.0.1:22; skipping failed SSH login attempts."
    return 0
  fi

  for ((i = 1; i <= tries; i++)); do
    timeout 8 ssh \
      -o ConnectTimeout=5 \
      -o NumberOfPasswordPrompts=1 \
      -o PreferredAuthentications=password \
      -o PubkeyAuthentication=no \
      -o KbdInteractiveAuthentication=no \
      -o StrictHostKeyChecking=no \
      -o UserKnownHostsFile=/dev/null \
      invaliduser@127.0.0.1 "exit" >/dev/null 2>&1 || true
  done
  echo "[OK] Failed SSH login attempts triggered: $tries"
}

run_failed_priv_esc_attempts() {
  local tries=2
  local i

  if command -v sudo >/dev/null 2>&1; then
    for ((i = 1; i <= tries; i++)); do
      printf '%s\n' "$BAD_PASSWORD" | sudo -S -k -p "" id >/dev/null 2>&1 || true
    done
    echo "[OK] Failed sudo privilege escalation attempts triggered: $tries"
  else
    echo "[WARN] sudo not found; skipping sudo attempts."
  fi

  if command -v su >/dev/null 2>&1; then
    printf '%s\n' "$BAD_PASSWORD" | timeout 8 su root -c "id" >/dev/null 2>&1 || true
    echo "[OK] Failed su privilege escalation attempt triggered: 1"
  else
    echo "[WARN] su not found; skipping su attempt."
  fi
}

show_new_log_lines() {
  local log_file="$1"
  local start_line="$2"

  if [[ -r "$log_file" ]]; then
    tail -n +"$start_line" "$log_file" | grep -Ei "sshd|failed|invalid user|sudo|su:|authentication failure|sudoers" || true
    return 0
  fi

  if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    sudo tail -n +"$start_line" "$log_file" | grep -Ei "sshd|failed|invalid user|sudo|su:|authentication failure|sudoers" || true
    return 0
  fi

  if command -v journalctl >/dev/null 2>&1; then
    journalctl --since "$START_TIME" --no-pager | grep -Ei "sshd|failed|invalid user|sudo|su:|authentication failure|sudoers" || true
    return 0
  fi

  echo "[WARN] Cannot read $log_file (insufficient permissions)."
  echo "Run this to inspect manually: sudo tail -n 80 \"$log_file\""
}

LOG_FILE="$TARGET_LOG_FILE"
if [[ -z "$LOG_FILE" ]]; then
  LOG_FILE="$(detect_log_file || true)"
fi

if [[ -z "$LOG_FILE" ]]; then
  echo "Error: no auth log file found (/var/log/auth.log or /var/log/secure)." >&2
  exit 1
fi

if [[ ! -f "$LOG_FILE" ]]; then
  echo "Error: log file not found: $LOG_FILE" >&2
  exit 1
fi

if [[ -r "$LOG_FILE" ]]; then
  START_LINE=$(( $(wc -l < "$LOG_FILE") + 1 ))
elif command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
  START_LINE=$(( $(sudo wc -l < "$LOG_FILE") + 1 ))
else
  START_LINE=1
fi

echo "Using auth log file: $LOG_FILE"
echo "Generating real events..."
START_TIME="$(date '+%Y-%m-%d %H:%M:%S')"
run_failed_ssh_attempts
run_failed_priv_esc_attempts
sleep 2

echo
echo "New suspicious lines from $LOG_FILE:"
show_new_log_lines "$LOG_FILE" "$START_LINE"
echo
echo "Now run: ./mini_hids.sh \"$LOG_FILE\""
