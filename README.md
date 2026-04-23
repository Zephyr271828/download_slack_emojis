# download_slack_emojis

Download all custom emoji from a Slack workspace (images + alias map) using the Slack Web API.

## Requirements

- Python 3.8+
- `requests` (`pip install requests`)

## 1. Create a Slack App

1. Go to <https://api.slack.com/apps> and click **Create New App** → **From scratch**.
2. Give it a name (e.g. `emoji-downloader`) and pick the workspace you want to pull emoji from.
3. Click **Create App**.

## 2. Add the required OAuth scope

The script calls `emoji.list`, which needs the `emoji:read` bot scope.

1. In the app settings sidebar, open **OAuth & Permissions**.

   ![OAuth & Permissions page](figs/oauth_permissions.png)

2. Scroll down to **Scopes** → **Bot Token Scopes** and click **Add an OAuth Scope**.
3. Add `emoji:read` — it should show up as below:

   ![emoji:read scope added](figs/emoji_read.png)

A bot token is sufficient for this script. If you'd rather use a user token, add `emoji:read` under **User Token Scopes** instead — either works as long as the token carries that scope.

## 3. Install the app to your workspace

1. Still on **OAuth & Permissions**, scroll to the top and click **Install to Workspace** (or **Reinstall to Workspace** if you've changed scopes).
2. Approve the permission prompt.
3. Copy the **Bot User OAuth Token** — it starts with `xoxb-...`. This is the token the script needs.

> Workspaces with admin approval enabled may require a workspace admin to approve the install before the token becomes active.

## 4. Configure the token

The script reads the token from a module-level constant `SLACK_BOT_TOKEN` in `download_slack_emoji.py`. The recommended pattern is to load it from the environment so the token doesn't end up in source control:

```python
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
```

Then export it before running:

```bash
export SLACK_BOT_TOKEN="xoxb-xxxx-xxxx-xxxx"
```

If you hardcode the token instead, **do not commit the file** — treat the token as a secret. If a token is ever leaked, rotate it by going to **OAuth & Permissions** → **Revoke Token** and reinstalling the app.

## 5. Run

```bash
python download_slack_emoji.py
```

Output:

- `outputs/` — one image file per custom emoji (extension preserved from the source URL, defaulting to `.png`).
- `outputs/aliases.txt` — lines of the form `alias_name -> target_name` for emoji that are aliases of other emoji.

The script prints progress for each download and a summary at the end:

```
Real emoji files: <N>
Aliases: <M>
Saved to: /abs/path/to/outputs
```

## Notes

- Only **custom** workspace emoji are returned by `emoji.list`; standard Unicode emoji are not included.
- `emoji.list` is rate-limited (Tier 2). For very large workspaces you may need to add retry/backoff.
- To change the output directory, edit the `OUTDIR` variable at the top of the script.
