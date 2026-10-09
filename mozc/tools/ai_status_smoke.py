"""隔離した実辞書/モデルのセッションでAI状態・計算量を確認する。実IMEには接続しない。"""
import argparse,hashlib,json,os,queue,re,subprocess,tempfile,threading,time
from pathlib import Path


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("exe",type=Path)
    ap.add_argument("--install",default=r"C:\Program Files (x86)\Kotori")
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    exe=args.exe.resolve()
    exe_hash=hashlib.sha256(exe.read_bytes()).hexdigest()
    env=dict(os.environ,KOTORI_MODEL_DIR=args.install,KOTORI_RUNTIME_DIR=args.install,
             KOTORI_LM_K="8",KOTORI_LM_PREDICT="0")
    samples=[]
    with tempfile.TemporaryDirectory(prefix="kotori-status-") as temp:
        profile=Path(temp)/"session"
        with args.out.with_suffix(".stderr.txt").open("wb") as err:
            p=subprocess.Popen([str(exe),"--dictionary=oss","--profile="+str(profile)],
                cwd=str(exe)+".runfiles/_main",env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err)
            lines=queue.Queue()
            def read():
                for line in p.stdout:lines.put(line.decode("utf-8").rstrip())
                lines.put(None)
            reader=threading.Thread(target=read,daemon=True);reader.start()
            def send(command):
                p.stdin.write((command+"\nSHOW_OUTPUT\n").encode("utf-8"));p.stdin.flush()
                tail=False;deadline=time.monotonic()+60
                while True:
                    line=lines.get(timeout=max(.01,deadline-time.monotonic()))
                    if line is None:raise RuntimeError("session exited: "+str(p.poll()))
                    if tail and line.strip()=="}":break
                    tail|=line.startswith("removed_candidate_words_for_debug {")
            try:
                send("SEND_KEY\tON\nSEND_KEYS\tashiwoitametanode")
                started=time.monotonic()
                while time.monotonic()-started<40:
                    status=profile/"kotori_ai_status.txt"
                    if status.exists():
                        kv=dict(line.split("=",1) for line in status.read_text(encoding="utf-8").splitlines() if "=" in line)
                        if not samples or kv!=samples[-1]["status"]:
                            samples.append({"seconds":time.monotonic()-started,"status":kv})
                        if kv.get("state") in ("llm","zenz"):
                            assert kv.get("pid")==str(p.pid)
                            assert int(kv["process_started"])>0
                            calls=re.findall(r"calls=(\d+)",kv["stats"])
                            if calls and sum(map(int,calls))>0:break
                        if kv.get("state")=="error":raise RuntimeError(str(kv))
                    time.sleep(.5)
                    send("KOTORI_REFRESH")
                else:raise AssertionError("AI state/counters did not update within 40 seconds")
                allowed={"state","message","device","zenz","llm","stats","pid","process_started"}
                assert all(set(s["status"])<=allowed for s in samples)
                assert hashlib.sha256(exe.read_bytes()).hexdigest()==exe_hash
                args.out.write_text(json.dumps({"exe":str(exe),"exe_sha256":exe_hash,
                    "scope":"isolated model/session telemetry, not installed TSF or GUI live server",
                    "samples":samples,"checks":{"pid_matches":True,"counters_positive":True,"no_input_fields":True}},
                    ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                print("AI status smoke PASS:",samples[-1]["status"])
                p.stdin.close();p.wait(timeout=60)
                assert p.returncode==0
            finally:
                if p.poll() is None:p.kill();p.wait()
                reader.join(timeout=2);p.stdout.close()


if __name__=="__main__":main()
