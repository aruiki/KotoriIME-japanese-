"""実セッションの初回候補と遅延更新を記録する。実行中の IME には接続しない。

変更後の session_handler_main が必要。SHOW_OUTPUT の末尾を待って応答時間を測る。
実際の TSF / アプリ上の遅延とは区別する。モデルはインストール先から読む。
"""
import argparse
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import tempfile
import threading
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("exe", type=Path)
    ap.add_argument("--install", default=r"C:\Program Files (x86)\Kotori")
    ap.add_argument("--romaji", default="ashiwoitametanode")
    ap.add_argument("--warm", type=float, default=12)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    exe = args.exe.resolve()
    lines = queue.Queue()
    env = dict(os.environ, KOTORI_MODEL_DIR=args.install,
               KOTORI_RUNTIME_DIR=args.install)
    with tempfile.TemporaryDirectory(prefix="kotori-first-") as profile:
        with args.out.with_suffix(".stderr.txt").open("wb") as err:
            p = subprocess.Popen(
                [str(exe), "--dictionary=oss", "--profile=" + str(Path(profile) / "session")],
                cwd=str(exe) + ".runfiles/_main", env=env,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err)

            def read():
                for line in p.stdout:
                    lines.put(line.decode("utf-8").rstrip())
                lines.put(None)

            reader = threading.Thread(target=read, daemon=True)
            reader.start()

            def send(command):
                started = time.monotonic()
                p.stdin.write((command + "\nSHOW_OUTPUT\n").encode("utf-8"))
                p.stdin.flush()
                output, tail = [], False
                deadline = started + 60
                while True:
                    line = lines.get(timeout=max(.01, deadline - time.monotonic()))
                    if line is None:
                        raise RuntimeError("session handler exited unexpectedly: " + "\n".join(output))
                    output.append(line)
                    if tail and line.strip() == "}":
                        break
                    tail |= line.startswith("removed_candidate_words_for_debug {")
                text = "\n".join(output)
                match = re.search(r'candidate_window \{.*?value: "([^"]*)"',
                                  text, re.S)
                return {"command": command,
                        "response_ms": (time.monotonic() - started) * 1000,
                        "first_candidate": match.group(1) if match else None,
                        "output": text}

            try:
                send("SEND_KEY\tON\nSEND_KEYS\tai")
                time.sleep(args.warm)
                send("SEND_KEY\tESC")
                rows = [send("SEND_KEYS\t" + args.romaji)]
                for delay in (.2, .8, .8, .8, .8):
                    time.sleep(delay)
                    rows.append(send("KOTORI_REFRESH"))
                rows.append(send("SEND_KEY\tSpace"))
                p.stdin.close()
                p.wait(timeout=60)
                if p.returncode:
                    raise RuntimeError(f"session handler exit {p.returncode}")
                args.out.write_text(json.dumps({"exe": str(exe),
                    "romaji": args.romaji, "warm_seconds": args.warm,
                    "events": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
                for row in rows:
                    print(f'{row["response_ms"]:.1f} ms: {row["first_candidate"]}')
            finally:
                if p.poll() is None:
                    p.kill()
                    p.wait()
                reader.join(timeout=2)
                p.stdout.close()


if __name__ == "__main__":
    main()
