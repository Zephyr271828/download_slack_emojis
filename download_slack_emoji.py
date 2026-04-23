import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
OUTDIR = Path("outputs")
OUTDIR.mkdir(exist_ok=True)

def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)

# 1) 取 emoji 列表
resp = requests.get(
    "https://slack.com/api/emoji.list",
    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
    timeout=30,
)
resp.raise_for_status()
data = resp.json()

if not data.get("ok"):
    raise RuntimeError(f"Slack API error: {data}")

emoji_map = data["emoji"]

real_emojis = {}
aliases = {}

for name, value in emoji_map.items():
    if isinstance(value, str) and value.startswith("alias:"):
        aliases[name] = value[len("alias:"):]
    else:
        real_emojis[name] = value

# 2) 下载真实图片
for name, url in real_emojis.items():
    parsed = urlparse(url)
    path_part = parsed.path

    ext = Path(path_part).suffix.lower()
    if not ext:
        ext = ".png"

    filename = safe_name(name) + ext
    outpath = OUTDIR / filename

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    outpath.write_bytes(r.content)
    print(f"downloaded: {outpath}")

# 3) 保存 alias 信息
alias_file = OUTDIR / "aliases.txt"
with alias_file.open("w", encoding="utf-8") as f:
    for alias_name, target_name in sorted(aliases.items()):
        f.write(f"{alias_name} -> {target_name}\n")

print()
print(f"Done.")
print(f"Real emoji files: {len(real_emojis)}")
print(f"Aliases: {len(aliases)}")
print(f"Saved to: {OUTDIR.resolve()}")