# Codex OAuth Troubleshooting

Use this guide when Codex CLI cannot authenticate or refresh a session. Authentication requires a human-operated browser; never paste the code, callback URL, or token into a repository, issue, prompt artifact, or chat transcript.

## Symptoms

- `codex login status` reports that you are not logged in.
- `codex exec` returns `401 Unauthorized` or an OAuth-refresh failure.
- The login status appears valid but a small Codex command still fails with an expired or already-used refresh token.

## Recovery

1. Check the current state:

   ```bash
   codex login status
   ```

2. End the stale session, then start device authentication:

   ```bash
   codex logout
   codex login --device-auth
   ```

3. Open the device-auth address and enter the displayed code in a local interactive browser. Complete any anti-bot challenge there; headless browser automation may be blocked.
4. Verify the repaired session:

   ```bash
   codex login status
   tmp="$(mktemp -d)"
   git -C "$tmp" init -q
   (cd "$tmp" && codex exec --ephemeral --skip-git-repo-check -s read-only 'Reply exactly CODEX_OK')
   ```

5. If the smoke test still fails, record only the non-secret error message and CLI version for further support:

   ```bash
   codex --version
   ```

## Safety

- The Codex CLI manages credentials under `~/.codex/`; do not copy those files into projects or share their contents.
- Do not use a browser session, a device code, or an OAuth callback as a substitute for a user-authorized login.
- A successful `codex login status` alone is not complete proof of a working session; the read-only smoke test verifies the actual command path.
