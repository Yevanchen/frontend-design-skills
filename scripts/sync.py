#!/usr/bin/env python3
"""Vendor selected upstream skills, or verify the recorded snapshot (Python 3 + Git)."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def inventory(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink: {path}")
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = {
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "executable": bool(path.stat().st_mode & 0o111),
            }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify local files without network or writes")
    parser.add_argument("--check-upstream", action="store_true", help="Also verify each recorded commit is current upstream HEAD")
    args = parser.parse_args()
    config = json.loads((ROOT / "sources.json").read_text())
    destination = ROOT / "skills" / config["category"]
    lock_path = ROOT / "sources.lock.json"
    if args.check or args.check_upstream:
        lock = json.loads(lock_path.read_text())
        if lock["config"] != config:
            raise ValueError("Source configuration changed; run scripts/sync.py")
        if inventory(destination) != lock["files"]:
            raise ValueError("Skill contents or executable permissions differ from the snapshot")
        if inventory(ROOT / "third-party") != lock["notices"]:
            raise ValueError("Upstream notices differ from the snapshot")
        for repo, source in lock["sources"].items():
            if args.check_upstream:
                current = git("ls-remote", f"https://github.com/{repo}.git", "HEAD").split()[0]
                if current != source["commit"]:
                    raise ValueError(f"Update available: {repo}: {source['commit']} -> {current}")
        print(f"Verified {len(lock['skills'])} skills, {len(lock['files'])} files" + ("; all upstream HEADs current" if args.check_upstream else ""))
        return

    # Fetch and validate every upstream in staging before replacing the published snapshot.
    with tempfile.TemporaryDirectory(prefix="frontend-design-skills-") as temp:
        stage = Path(temp)
        skills = stage / "skills"
        notices = stage / "third-party"
        skills.mkdir()
        notices.mkdir()
        lock = {"version": 1, "syncedAt": datetime.now(timezone.utc).isoformat(), "config": config, "sources": {}, "skills": {}}
        for index, (repo, spec) in enumerate(config["sources"].items()):
            checkout = stage / f"upstream-{index}"
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", f"https://github.com/{repo}.git", str(checkout)], check=True)
            commit = git("-C", str(checkout), "rev-parse", "HEAD")
            lock["sources"][repo] = {"commit": commit}
            for name, relative in spec["skills"].items():
                original = checkout / relative
                text = (original / "SKILL.md").read_text()
                if f"name: {name}" not in text.splitlines():
                    raise ValueError(f"Skill name mismatch: {repo}/{relative}")
                shutil.copytree(original, skills / name)
                lock["skills"][name] = {"source": repo, "path": relative, "commit": commit}
            notice_dir = notices / repo.replace("/", "--")
            notice_dir.mkdir()
            for relative in spec["notices"]:
                shutil.copy2(checkout / relative, notice_dir / Path(relative).name)
            print(f"Synced {repo} @ {commit[:12]} ({len(spec['skills'])} skills)")
        lock["files"] = inventory(skills)
        lock["notices"] = inventory(notices)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(skills, destination)
        if (ROOT / "third-party").exists():
            shutil.rmtree(ROOT / "third-party")
        shutil.copytree(notices, ROOT / "third-party")
        lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n")
        print(f"Updated {len(lock['skills'])} skills. Review the diff before committing.")


if __name__ == "__main__":
    main()
