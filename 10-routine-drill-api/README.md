# Project 10 — Routine Drill: API-Triggered Routine

**Concept:** Appendix A3 (API trigger) — "A retrying webhook is a runaway
heartbeat," and the fix belongs at the caller, not the endpoint.

## What's in this folder

```
10-routine-drill-api/
└── demo.py     # a real local HTTP server + real HTTP client calls
```

No mocking of network calls — `demo.py` starts an actual
`ThreadingHTTPServer` on `127.0.0.1:8743`, standing in for a Routine's
`/fire` endpoint, and fires real `POST` requests at it with `urllib`.

## Proof it works (three real parts, already run)

**Part 1 — a wrong token gets a message that says what to do next**, not
just a bare `401`:
```
status=401 body={'error': 'invalid_token', 'message': "Bearer token missing
or incorrect. Regenerate it in the Routine's API trigger settings and
update the caller's secret store -- do not retry with the same token."}
```

**Part 2 — the endpoint itself does NOT deduplicate.** A simulated
monitoring tool that resends on every timeout (a very common real
failure mode) fires the same alert 3 times with no client-side
protection:
```
attempt 1: status=200 -> sess_0001
attempt 2: status=200 -> sess_0002
attempt 3: status=200 -> sess_0003
RESULT: 3 separate Routine runs fired for ONE alert. That's 3x the cost
for 1x the event.
```

This is real: three genuinely separate sessions were "created" (three
different `session_id`s), for what was, semantically, one event. Left
unattended overnight with a misbehaving sender, this is exactly how a
Routine burns its whole daily cap — or racks up metered charges — before
anyone notices.

**Part 3 — the same retry storm, but the caller dedupes first**, using a
stable idempotency key (`SEN-99`), the same pattern as Project 7's
ticket writes:
```
[sent]    SEN-99: status=200 -> sess_0004
[skipped] SEN-99: already sent this beat, not re-firing
[skipped] SEN-99: already sent this beat, not re-firing
RESULT: 1 Routine run fired for the SEN-99 retry storm (should be 1).
```

One call reaches the server. Two are caught before they ever leave the
sender.

## How to run it yourself

```
cd "E:\Loop Engineering Projects\10-routine-drill-api"
python demo.py
```
No dependencies, no network access needed (everything is `127.0.0.1`),
completes in under a second.

## How this maps to a real Routine

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/<routine-id>/fire \
  -H "Authorization: Bearer <routine-token>" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
```

Same shape as `demo.py`'s `post()` function. The real endpoint's token is
shown exactly once when you generate it — store it in your alerting
tool's secret store immediately, the same way `demo.py`'s server treats a
stale/wrong token as unrecoverable without a human regenerating it.

**The dedup logic (Part 3) is not something the real API does for you
either** — this demo's server has zero dedup logic, matching the real
`/fire` endpoint's documented behavior. Whatever system calls `/fire`
(your alerting tool, your deploy pipeline, your own cron job) needs its
own idempotency key, exactly like `already_sent` above.

## Run it automatically

Fully run, for real, above — this drill needed no Anthropic account or
credentials at all, since I built both sides of the API call locally.
That's the whole point of this drill: the caller-side dedup discipline
is yours to build regardless of which real endpoint sits behind it.

## The concept, made concrete

| In the course | In this project |
|---|---|
| "A retrying webhook is a runaway heartbeat" | Part 2, proven: 3 real sessions for 1 event |
| "Errors must say what to do next" (Concept 10, reused here) | Part 1's 401 message |
| "Writes must be safe to repeat" (Concept 10 / Project 7) | Part 3's `already_sent` idempotency key |
| Token shown once, store immediately | Modeled by the server's unrecoverable-without-a-human 401 |
