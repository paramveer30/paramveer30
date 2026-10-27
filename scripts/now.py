"""Render assets/now-{dark,light}.svg from recent public GitHub activity.

Runs in a scheduled workflow so the profile never goes stale.
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone
from string import Template

sys.path.insert(0, os.path.dirname(__file__))
from gen import THEMES, T, e, svg  # noqa: E402

USER = os.environ.get("GH_USER", "paramveer30")
ROWS = 5


def fetch():
    req = urllib.request.Request(f"https://api.github.com/users/{USER}/events/public?per_page=100",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": USER})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def rows_from(events):
    out, seen = [], set()
    for ev in events:
        repo = ev["repo"]["name"].split("/")[-1]
        if repo == USER:
            continue
        ts = datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00"))
        p = ev.get("payload", {})
        if ev["type"] == "PushEvent":
            for c in reversed(p.get("commits", [])):
                msg = c["message"].splitlines()[0]
                key = (repo, msg)
                if key in seen:
                    continue
                seen.add(key)
                out.append((ts, "push", repo, msg))
        elif ev["type"] == "CreateEvent" and p.get("ref_type") == "repository":
            out.append((ts, "init", repo, p.get("description") or "new repository"))
        elif ev["type"] == "PullRequestEvent" and p.get("action") in ("opened", "closed"):
            out.append((ts, "pr", repo, p["pull_request"]["title"]))
        elif ev["type"] == "ReleaseEvent":
            out.append((ts, "release", repo, p["release"].get("name") or p["release"]["tag_name"]))
    out.sort(key=lambda r: r[0], reverse=True)
    return out[:ROWS]



def clip(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


def render(rows, now):
    W = 1000
    H = 74 + max(1, len(rows)) * 30 + 20
    kind_col = {"push": "$l4", "init": "$l2", "pr": "$l1", "release": "$l3"}
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="$panel" stroke="$border"/>',
         '<circle class="rx" cx="30" cy="25" r="5" fill="$ok"/>',
         T(44, 29, "RX", 11, "$ok", weight=700),
         T(70, 29, e(f"uart0 · 115200 baud · live from github.com/{USER}"), 11, "$dim"),
         T(W - 24, 29, e("last tx " + (rows[0][0].strftime("%Y-%m-%d") if rows else "none")), 11, "$dim", "end"),
         f'<line x1="16" y1="42" x2="{W-16}" y2="42" stroke="$faint"/>']
    if not rows:
        b.append(T(30, 80, "waiting for the next push…", 13, "$dim"))
    for i, (ts, kind, repo, msg) in enumerate(rows):
        y = 74 + i * 30
        c = kind_col[kind]
        g = [T(30, y, e(ts.strftime("%b %d").lower()), 12, "$dim"),
             f'<rect x="110" y="{y-14}" width="62" height="20" rx="4" fill="none" stroke="{c}"/>',
             T(141, y, kind, 11, c, "middle", 700),
             T(188, y, e(clip(repo, 26)), 13, "$fg", weight=700),
             T(420, y, e(clip(msg, 72)), 12.5, "$dim")]
        b.append(f'<g class="ln" style="animation-delay:{i*0.35:.2f}s">{"".join(g)}</g>')
    y = 74 + max(1, len(rows)) * 30
    b.append(T(30, y, "&gt;", 13, "$fg"))
    b.append(f'<rect class="blink" x="44" y="{y-11}" width="8" height="14" fill="$l4"/>')
    css = (".rx{animation:rx 1.6s steps(1) infinite}@keyframes rx{0%,10%,20%{opacity:1}5%,15%,60%{opacity:.25}}"
           ".ln{opacity:0;animation:ln .5s ease-out forwards}@keyframes ln{to{opacity:1}}")
    label = "Recent activity: " + "; ".join(f"{k} to {r}: {m}" for _, k, r, m in rows)
    return svg(W, H, label, "".join(b), css)


def main(out="assets"):
    now = datetime.now(timezone.utc)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            events = json.load(f)
    else:
        events = fetch()
    tpl = Template(render(rows_from(events), now))
    os.makedirs(out, exist_ok=True)
    for th, vals in THEMES.items():
        with open(os.path.join(out, f"now-{th}.svg"), "w") as f:
            f.write(tpl.substitute(vals))


if __name__ == "__main__":
    main()
