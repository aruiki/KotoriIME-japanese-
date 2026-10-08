"""GitHubの使い捨てWindowsランナーで、MSIの導入・実入力・削除を確認する。

開発者の普段のIMEを変更しないため、GitHub Actions外では実行を拒否する。
既存のKotoriがあるランナーでも実行しない。結果とMSIログを出力先へ保存する。
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def run(command, timeout=180):
    p = subprocess.run(command, capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"exit {p.returncode}: {command[0]}\n" +
                           p.stdout.decode("utf-8", "replace") +
                           p.stderr.decode("utf-8", "replace"))
    return p


def msi_property(msi, name):
    # MSI のファイルパスを /x に渡すと、Windows Installer が再び媒体を
    # 開こうとして時間がかかることがある。ProductCodeで削除する。
    script = ("$wi=New-Object -ComObject WindowsInstaller.Installer;"
              "$db=$wi.GetType().InvokeMember('OpenDatabase','InvokeMethod',$null,$wi,@('"
              + str(msi).replace("'", "''") + "',0));"
              "$v=$db.OpenView(\"SELECT Value FROM Property WHERE Property='"
              + name + "'\");$v.Execute();$r=$v.Fetch();$r.StringData(1)")
    p = subprocess.run(["powershell", "-NoProfile", "-Command", script],
                       capture_output=True, text=True, check=True, timeout=30)
    value = p.stdout.strip()
    if not value:
        raise RuntimeError(f"MSIの{name}が空です")
    return value


def run_msi(arguments, log):
    """ランナーが停止しても原因の手掛かりが残るようMSIの段階を逐次記録する。"""
    process = subprocess.Popen(["msiexec", *arguments, "/qn", "/norestart",
                                "/L*vx!", str(log)])
    start = time.monotonic()
    offset = 0
    try:
        while True:
            if log.exists():
                with log.open("r", encoding="utf-16", errors="replace") as stream:
                    stream.seek(offset)
                    for line in stream:
                        if any(key in line for key in ("Action start", "Action ended",
                                "RESTART MANAGER", "Restart", "Return value 3",
                                "MainEngineThread")):
                            print(line.rstrip(), flush=True)
                    offset = stream.tell()
            code = process.poll()
            if code is not None:
                return code
            if time.monotonic() - start > 300:
                raise subprocess.TimeoutExpired("msiexec", 300)
            time.sleep(1)
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=15)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--msi", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if (sys.platform != "win32" or os.environ.get("GITHUB_ACTIONS") != "true" or
            os.environ.get("KOTORI_DISPOSABLE_RUNNER") != "github-hosted"):
        raise RuntimeError("使い捨てのGitHub Actions Windowsランナーでのみ実行できます")
    install = Path(os.environ["ProgramFiles(x86)"]) / "Kotori"
    if install.exists():
        raise RuntimeError("既存のKotoriがあるので停止します")
    msi, out = args.msi.resolve(), args.out.resolve()
    if not msi.is_file():
        raise FileNotFoundError(msi)
    out.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parents[2] / "eval" / "imebench" / "ImeBench.cs"
    # __file__ は repo/mozc/tools。リポジトリ直下は parents[2]。
    with msi.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    result = {"msi": msi.name, "sha256": digest,
              "source_commit": os.environ.get("GITHUB_SHA"),
              "run_id": os.environ.get("GITHUB_RUN_ID"),
              "install": False, "input": False, "uninstall": False}
    errors = []
    result["product_code"] = msi_property(msi, "ProductCode")

    def checkpoint(stage):
        result["stage"] = stage
        result["errors"] = errors
        text = json.dumps(result, ensure_ascii=False, indent=2)
        (out / "result.json").write_text(text, encoding="utf-8")
        print(text, flush=True)

    attempted = False
    try:
        attempted = True
        checkpoint("installing")
        code = run_msi(["/i", str(msi)], out / "install.log")
        result["install_exit"] = code
        if code != 0:
            raise RuntimeError(f"導入の終了コード: {code}（3010は再起動が必要）")
        for name in ("mozc_server.exe", "mozc_renderer.exe", "mozc_tip64.dll"):
            if not (install / name).is_file():
                raise RuntimeError(f"導入後のファイルがありません: {name}")
        result["install"] = True
        checkpoint("installed")
        exe = out / "ImeBench.exe"
        compiler = Path(os.environ["WINDIR"]) / "Microsoft.NET/Framework64/v4.0.30319/csc.exe"
        run([str(compiler), "/nologo", "/target:winexe", "/platform:x64",
             "/reference:System.Windows.Forms.dll", "/reference:System.Drawing.dll",
             "/out:" + str(exe), str(source)])
        cases = out / "input.tsv"
        cases.write_text("warm\tnihonngo\n0\tnihonngo\n1\ttoukyou\n", encoding="utf-8")
        output = out / "output.tsv"
        run([str(exe), "{2A1ADAE4-8061-4AC0-A7D4-713BF8DCB591}",
             "{455A87E7-275F-4582-92CB-6600917A436D}", str(cases), str(output), "3000"])
        error = Path(str(output) + ".error.txt")
        if error.exists():
            raise RuntimeError(error.read_text(encoding="utf-8-sig"))
        got = dict(line.split("\t", 1) for line in output.read_text(encoding="utf-8-sig").splitlines()
                   if "\t" in line)
        result["committed_text"] = got
        if got.get("0") != "日本語" or got.get("1") != "東京":
            raise RuntimeError(f"実入力の結果が一致しません: {got}")
        result["input"] = True
        checkpoint("input_verified")
    except Exception as exc:
        errors.append(str(exc))
    finally:
        if attempted:
            try:
                checkpoint("uninstalling")
                # この検証で入れたフォルダのプロセスだけを停止し、削除時のロックを外す。
                script = "$root = [IO.Path]::GetFullPath($env:KOTORI_SMOKE_INSTALL) + '\\'; " + \
                         "Get-Process | Where-Object { $_.Path -and $_.Path.StartsWith($root, [StringComparison]::OrdinalIgnoreCase) } | Stop-Process -Force"
                env = dict(os.environ, KOTORI_SMOKE_INSTALL=str(install))
                subprocess.run(["powershell", "-NoProfile", "-Command", script], env=env,
                               capture_output=True, timeout=30, check=True)
                code = run_msi(["/x", result["product_code"]], out / "uninstall.log")
                result["uninstall_exit"] = code
                result["reboot_required"] = code == 3010
                result["uninstall"] = code in (0, 3010) and not (install / "mozc_tip64.dll").exists()
                if not result["uninstall"]:
                    errors.append("アンインストールの完了を確認できません")
            except Exception as exc:
                errors.append("削除確認: " + str(exc))
        checkpoint("finished")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
