#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual/Triple-Repository Skills Synchronization Engine
Maintains perfect byte-for-byte synchronization of skills across:
1. Agent Command Center (https://github.com/HunterHill13/Motion-Graphic-Agent.git)
   - Central Skills Library: `skills/` and `.agents/skills/`
2. Motion-Graphic-Namoosi Engine (https://github.com/HunterHill13/Motion-Graphic-Namoosi.git)
   - Advanced Opus 5.5 / mg-styles-15 Skill: `.agents/skills/Motion-Graphic-Namoosi/`
3. Classic Remotion Skill Engine (https://github.com/HunterHill13/Cinematic-Motion-Graphics-Agent-Skill-Plan.git)
   - Classic Remotion Skill: `.agents/skills/cinematic-motion-director/` (commit c75afa1)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Force UTF-8 on Windows consoles to prevent UnicodeEncodeError with Persian folder names
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def get_repo_roots():
    script_dir = Path(__file__).resolve().parent
    current_repo = script_dir.parent
    
    # Locate sibling repositories
    parent_dir = current_repo.parent
    candidate_agent = parent_dir / "Motion-Graphic-Agent"
    candidate_namoosi = parent_dir / "اسکیل موشن گرافیک"
    candidate_classic = parent_dir / "Cinematic-Motion-Graphics-Agent-Skill-Plan"
    
    return {
        "current": current_repo,
        "agent": candidate_agent if candidate_agent.exists() else None,
        "namoosi": candidate_namoosi if candidate_namoosi.exists() else None,
        "classic": candidate_classic if candidate_classic.exists() else None,
        "skill": candidate_namoosi if candidate_namoosi.exists() else candidate_classic,
    }

def run_git(repo_path, args):
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="replace"
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def sync_all_skills(roots, direction="skill_to_agent"):
    agent_repo = roots["agent"]
    namoosi_repo = roots["namoosi"]
    classic_repo = roots["classic"]
    
    if not (agent_repo and agent_repo.exists()):
        return False
        
    ignore_patterns = shutil.ignore_patterns(
        "*.mp4", "*.mov", "*.avi", "*.mkv", "*.ttf", "*.otf", "*.woff*",
        "previews", "fonts", "music", "node_modules", ".cache", "__pycache__"
    )
    
    # 1. Sync Motion-Graphic-Namoosi
    if namoosi_repo and namoosi_repo.exists():
        skill_src = namoosi_repo / ".agents" / "skills" / "Motion-Graphic-Namoosi"
        agent_dst_1 = agent_repo / "skills" / "Motion-Graphic-Namoosi"
        agent_dst_2 = agent_repo / ".agents" / "skills" / "Motion-Graphic-Namoosi"
        if direction == "skill_to_agent" and skill_src.exists():
            print(f"[sync] Syncing Motion-Graphic-Namoosi: {namoosi_repo.name} -> {agent_repo.name}...")
            for dst in [agent_dst_1, agent_dst_2]:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists(): shutil.rmtree(dst)
                shutil.copytree(skill_src, dst, ignore=ignore_patterns)
            print("  ✅ Synced Motion-Graphic-Namoosi into Agent library.")
        elif direction == "agent_to_skill":
            src = agent_dst_1 if agent_dst_1.exists() else agent_dst_2
            if src.exists():
                skill_src.parent.mkdir(parents=True, exist_ok=True)
                if skill_src.exists(): shutil.rmtree(skill_src)
                shutil.copytree(src, skill_src, ignore=ignore_patterns)
                print("  ✅ Synced Motion-Graphic-Namoosi into dedicated skill repository.")

    # 2. Sync cinematic-motion-director (classic Remotion)
    if classic_repo and classic_repo.exists():
        skill_src = classic_repo / ".agents" / "skills" / "cinematic-motion-director"
        agent_dst_1 = agent_repo / "skills" / "cinematic-motion-director"
        agent_dst_2 = agent_repo / ".agents" / "skills" / "cinematic-motion-director"
        if direction == "skill_to_agent" and skill_src.exists():
            print(f"[sync] Syncing cinematic-motion-director: {classic_repo.name} -> {agent_repo.name}...")
            for dst in [agent_dst_1, agent_dst_2]:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists(): shutil.rmtree(dst)
                shutil.copytree(skill_src, dst, ignore=ignore_patterns)
            print("  ✅ Synced cinematic-motion-director into Agent library.")
        elif direction == "agent_to_skill":
            src = agent_dst_1 if agent_dst_1.exists() else agent_dst_2
            if src.exists():
                skill_src.parent.mkdir(parents=True, exist_ok=True)
                if skill_src.exists(): shutil.rmtree(skill_src)
                shutil.copytree(src, skill_src, ignore=ignore_patterns)
                print("  ✅ Synced cinematic-motion-director into classic skill repository.")

    # 3. Keep internal agent_repo skills/ and .agents/skills/ in sync
    src_lib = agent_repo / "skills"
    dst_lib = agent_repo / ".agents" / "skills"
    if src_lib.exists():
        for s in src_lib.iterdir():
            if s.is_dir():
                dst_s = dst_lib / s.name
                if dst_s.exists(): shutil.rmtree(dst_s)
                shutil.copytree(s, dst_s, ignore=ignore_patterns)

    return True

def sync_pull():
    roots = get_repo_roots()
    print("=" * 60)
    print("DUAL-REPOSITORY PULL SYNCHRONIZATION")
    print("=" * 60)
    
    for key, repo in [("Agent Repo", roots["agent"]), ("Skill Repo", roots["skill"])]:
        if repo and repo.exists():
            print(f"\n[git] Pulling latest changes in {key} ({repo.name})...")
            code, out, err = run_git(repo, ["pull", "origin", "main"])
            if code == 0:
                print(f"  {out if out else 'Up to date'}")
            else:
                print(f"  Warning: {err}")
                
    if roots["agent"]:
        sync_all_skills(roots, direction="skill_to_agent")
        
    print("\n✅ Pull and synchronization complete.")

def sync_push(commit_msg):
    roots = get_repo_roots()
    print("=" * 60)
    print("MULTI-REPOSITORY PUSH SYNCHRONIZATION")
    print("=" * 60)
    print(f"Message: {commit_msg}\n")
    
    current = roots["current"]
    agent_repo = roots["agent"]
    
    # 1. Mirror locally
    if roots["agent"]:
        if current == agent_repo:
            sync_all_skills(roots, direction="agent_to_skill")
        else:
            sync_all_skills(roots, direction="skill_to_agent")
            
    # 2. Commit and push in both repositories
    repos = [r for r in [agent_repo, skill_repo] if r and r.exists()]
    for repo in repos:
        print(f"\n[git] Processing {repo.name}...")
        if repo == agent_repo:
            run_git(repo, ["add", "skills", ".agents/skills", "scripts/sync_skills.py", ".gitignore"])
        else:
            run_git(repo, ["add", ".agents/skills/cinematic-motion-director", "scripts/sync_skills.py", ".gitignore"])
            
        code, out, _ = run_git(repo, ["diff", "--cached", "--name-only"])
        if not out:
            print(f"  Notice: No changes to commit in {repo.name}.")
            continue
            
        code, out, err = run_git(repo, ["commit", "-m", commit_msg])
        if code != 0:
            print(f"  Commit note: {err}")
            
        print(f"  Pushing to origin main ({repo.name})...")
        code, out, err = run_git(repo, ["push", "origin", "main"])
        if code == 0:
            print(f"  ✅ Successfully pushed {repo.name} to GitHub!")
        else:
            print(f"  Push warning: {err}")
            
    print("\n" + "=" * 60)
    print("✅ DUAL SYNCHRONIZATION FINISHED")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/sync_skills.py pull")
        print("  python scripts/sync_skills.py push <commit-message>")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    if action == "pull":
        sync_pull()
    elif action == "push":
        msg = sys.argv[2] if len(sys.argv) > 2 else "chore(skills): synchronize skills library across repositories"
        sync_push(msg)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
