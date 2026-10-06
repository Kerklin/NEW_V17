# V17 save step: merges this run's PUBLIC files (jobs.json, README.md) with anything changed on GitHub meanwhile,
# then pushes. Never force-pushes. Keeps your own edits to other files.
import json, os, shutil, subprocess, sys, time
from pathlib import Path
BR = os.environ.get("GITHUB_REF_NAME", "main") or "main"
TMP = Path(os.environ.get("RUNNER_TEMP", ".")) / "v17-save"
def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True)
if not Path("jobs.json").exists(): print("Nothing to save."); sys.exit(0)
git("config", "user.name", "job-agent"); git("config", "user.email", "job-agent@users.noreply.github.com")
shutil.rmtree(TMP, ignore_errors=True); TMP.mkdir(parents=True)
for p in ("jobs.json", "README.md"):
    if Path(p).exists(): shutil.copy2(p, TMP / p)
k = lambda j: (j.get("link", "") + "|" + j.get("title", "")).lower()
hb = git("show", "HEAD:jobs.json")
try: BASE = {k(j): j for j in json.loads(hb.stdout).get("jobs", [])} if hb.returncode == 0 else {}
except Exception: BASE = {}
def merge(mine, theirs):
    if not theirs: return mine
    have = {k(j): j for j in mine["jobs"]}
    for o in theirs.get("jobs", []):
        if BASE.get(k(o)) == o or k(o) in have: continue
        if k(o) not in BASE: mine["jobs"].append(o)          # added meanwhile by another run
    for n, s in theirs.get("meta", {}).get("sources", {}).items():
        m = mine["meta"].setdefault("sources", {}).setdefault(n, s)
        if s.get("last_ok", "") > m.get("last_ok", ""): m["last_ok"] = s["last_ok"]
    return mine
for attempt in range(1, 4):
    git("fetch", "--quiet", "origin", BR)
    th = git("show", f"origin/{BR}:jobs.json")
    try: theirs = json.loads(th.stdout) if th.returncode == 0 else None
    except Exception: theirs = None
    mine = merge(json.loads((TMP / "jobs.json").read_text(encoding="utf-8")), theirs)
    git("reset", "--quiet", "--hard", f"origin/{BR}")
    Path("jobs.json").write_text(json.dumps(mine, ensure_ascii=False, indent=1), encoding="utf-8")
    if (TMP / "README.md").exists(): shutil.copy2(TMP / "README.md", "README.md")
    git("add", "--", "jobs.json", "README.md")
    if git("diff", "--cached", "--quiet").returncode == 0: print("Nothing changed."); sys.exit(0)
    git("commit", "--quiet", "-m", "agent update")
    if git("push", "--quiet", "origin", f"HEAD:{BR}").returncode == 0: print(f"Saved (attempt {attempt})."); sys.exit(0)
    time.sleep(5 * attempt)
print("Could not save after 3 tries."); sys.exit(1)
