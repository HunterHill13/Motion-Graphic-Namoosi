#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Memory Synchronization Engine
Synchronizes memory/motion-director-memory.md and AGENTS.md with Git repository.
"""

import os
import sys
import subprocess
from pathlib import Path

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def run_git(cmd):
    try:
        res = subprocess.run(
            ["git"] + cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def pull_memory():
    print("[sync_agent_memory] Pulling latest memory updates...")
    ok, stdout, stderr = run_git(["pull", "--rebase"])
    if ok:
        print("[sync_agent_memory] Memory pull successful.")
    else:
        print(f"[sync_agent_memory] Pull warning (ignoring if clean): {stderr}")

def push_memory(commit_msg):
    print(f"[sync_agent_memory] Committing and pushing memory: {commit_msg}")
    run_git(["add", "memory/motion-director-memory.md", "AGENTS.md", "SKILL.md"])
    ok, stdout, stderr = run_git(["commit", "-m", commit_msg])
    if not ok and "nothing to commit" not in stdout + stderr:
        print(f"[sync_agent_memory] Commit note: {stdout or stderr}")
    ok_push, p_out, p_err = run_git(["push", "origin", "main"])
    if ok_push:
        print("[sync_agent_memory] Push to remote successful.")
    else:
        print(f"[sync_agent_memory] Push note: {p_err or p_out}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/sync_agent_memory.py [pull|push] [commit_message]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    if action == "pull":
        pull_memory()
    elif action == "push":
        msg = sys.argv[2] if len(sys.argv) > 2 else "chore(memory): update motion director memory"
        push_memory(msg)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
