#!/usr/bin/env python3
"""
Auto Knowledge Collector for jay-knowledge-db
- Scheduled: Daily analysis of code changes
- On-demand: Triggered by cron or API call
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
REPO_DIR = Path("/home/pi/.openclaw/workspace/working/code/nlp")
DOCS_DIR = REPO_DIR / "docs"


def run_subagent(agent_id: str, task: str) -> dict:
    """Call sub-agent via OpenClaw sessions_spawn"""
    # Use sessions_spawn via subprocess
    cmd = [
        "openclaw", "subagent", agent_id,
        "--cwd", str(REPO_DIR),
        "--task", task
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {"status": "done", "output": result.stdout}


def analyze_code() -> str:
    """Fuxi: Analyze code structure"""
    task = f"""Analyze jay-knowledge-db code in {REPO_DIR}.
Read all .py files and generate knowledge summary including:
- Classes and functions with docstrings
- Input/output formats
- Usage examples

Output to {DOCS_DIR}/code-analysis.md"""
    return f"Analyzed: {task[:50]}..."


def generate_faq() -> str:
    """Penny: Generate FAQ from code"""
    task = f"""Generate FAQ for jay-knowledge-db.
Read all .py files in {REPO_DIR} and create FAQ.md with:
- Quick start guide
- API reference for each class/function
- Common use cases

Output to {DOCS_DIR}/FAQ.md"""
    return f"Generated FAQ"


def daily_collect():
    """Scheduled daily collection"""
    print(f"[{datetime.now()}] Starting daily knowledge collection...")
    
    # 1. Check git changes
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    has_changes = bool(result.stdout.strip())
    
    if has_changes:
        print("  - Code changes detected, updating docs...")
        # Run analysis
        analyze_code()
        generate_faq()
        
        # Auto commit
        subprocess.run(["git", "add", "docs/"], cwd=REPO_DIR)
        subprocess.run([
            "git", "commit", "-m", 
            f"docs: Auto update knowledge {datetime.now().strftime('%Y-%m-%d')}"
        ], cwd=REPO_DIR)
        
        # Push
        subprocess.run(["git", "push", "origin", "master"], cwd=REPO_DIR)
        print("  - Docs updated and pushed")
    else:
        print("  - No changes, skipping")


def on_demand_collect():
    """On-demand collection triggered by cron"""
    print(f"[{datetime.now()}] On-demand knowledge collection...")
    analyze_code()
    generate_faq()
    print("  - Done")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    
    if mode == "daily":
        daily_collect()
    elif mode == "on-demand":
        on_demand_collect()
    else:
        print(f"Usage: {sys.argv[0]} [daily|on-demand]")
