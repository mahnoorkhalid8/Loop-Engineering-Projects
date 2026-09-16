#!/usr/bin/env python3
"""Simulates a Routine's API trigger (Appendix A3: POST /fire with a
bearer token) to prove two things for real, locally, with a real HTTP
server and real HTTP requests:

  1. The /fire endpoint itself does NOT deduplicate -- a retrying
     webhook really does cause repeat beats (Appendix A3's warning:
     "A retrying webhook is a runaway heartbeat").
  2. The fix belongs at the CALLER: dedupe before sending, using a
     stable idempotency key, exactly like Project 7's ticket writes.

Stdlib only (http.server + urllib).
"""

import json
import threading
import time
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = "routine-demo-token-abc123"
PORT = 8743
URL = f"http://127.0.0.1:{PORT}/fire"

fires_log = []          # every accepted call, in order -- the "runs" this Routine did
lock = threading.Lock()


class FireHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # quiet -- we print our own summary

    def do_POST(self):
        if self.path != "/fire":
            self.send_response(404)
            self.end_headers()
            return

        auth = self.headers.get("Authorization", "")
        if auth != f"Bearer {TOKEN}":
            body = json.dumps({
                "error": "invalid_token",
                "message": "Bearer token missing or incorrect. Regenerate it "
                           "in the Routine's API trigger settings and update "
                           "the caller's secret store -- do not retry with "
                           "the same token."
            }).encode()
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")

        with lock:
            session_id = f"sess_{len(fires_log) + 1:04d}"
            fires_log.append({"session_id": session_id, "text": payload.get("text", "")})

        body = json.dumps({
            "session_id": session_id,
            "url": f"https://claude.ai/code/routines/demo/{session_id}",
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def post(text: str, token: str = TOKEN):
    data = json.dumps({"text": text}).encode()
    req = urllib.request.Request(URL, data=data, method="POST", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), FireHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(0.3)

    print("### PART 1: bad token -> a clear, actionable error ###")
    status, resp = post("Sentry alert SEN-1: prod 500 spike", token="wrong-token")
    print(f"status={status} body={resp}\n")

    print("### PART 2: a retrying webhook with NO client-side dedup ###")
    print("(simulates a monitoring tool that resends on every timeout, 3x)")
    for i in range(3):
        status, resp = post("Sentry alert SEN-42: checkout latency > 2s")
        print(f"  attempt {i+1}: status={status} -> {resp['session_id']}")
    with lock:
        count_after_naive = len(fires_log)
    print(f"RESULT: {count_after_naive} separate Routine runs fired for ONE alert. "
          f"That's 3x the cost for 1x the event.\n")

    print("### PART 3: same retry storm, but the CALLER dedupes first ###")
    already_sent = set()  # the caller's own idempotency memory

    def send_once(alert_id: str, text: str):
        if alert_id in already_sent:
            print(f"  [skipped] {alert_id}: already sent this beat, not re-firing")
            return
        status, resp = post(text)
        already_sent.add(alert_id)
        print(f"  [sent]    {alert_id}: status={status} -> {resp['session_id']}")

    for i in range(3):  # same retry storm, same alert_id every time
        send_once("SEN-99", "Sentry alert SEN-99: DB connection pool exhausted")

    with lock:
        count_after_safe = len(fires_log)
    fired_for_sen99 = count_after_safe - count_after_naive
    print(f"RESULT: {fired_for_sen99} Routine run fired for the SEN-99 retry storm "
          f"(should be 1).\n")

    print("### full fires.log (every call the /fire endpoint actually accepted) ###")
    for f in fires_log:
        print(f"  {f['session_id']}: {f['text']}")

    server.shutdown()


if __name__ == "__main__":
    main()
