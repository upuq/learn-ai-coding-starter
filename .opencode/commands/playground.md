---
description: Start or reuse the Sloperator playground server on a port
---

Start the Sloperator playground on port `$ARGUMENTS` (use `8080` when no port is given).

Current TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

Before starting anything, check the listener list for an existing Sloperator playground server on that port. If one is already listening, reuse it and report its URL instead of starting another server.

If no Sloperator server is listening on the port, start `uv run playground/server.py <port>` in the background, then report the URL. Use the chosen port in place of `<port>`. Do not start a second server when one is already running.
