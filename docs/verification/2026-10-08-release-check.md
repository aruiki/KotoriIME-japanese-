# 公開前の追加確認 (2026-10-08)

対象ソース: PR138、5ba2de76995307ccd7bdd843ff975b71a409cf1b。
過去の検証記録を置き換えず、追加で実行した結果を記録する。

## 変換精度

`mozc/eval_baseline.py --context --out <result> --timeout 900` を前後の変換器で順に実行。
Standard、同じモデル、beams=4、LLM top=4、preload=0。各10コマンド終了コード0。
前は既存 `C:\Users\aruik\mz`、後は分離した `C:\Users\aruik\mzfi` のconverter_main.exe。
データ・変換器・モデル・環境のハッシュ等は各JSONのmanifestに保存した。

| データ | 変更前 | 変更後 |
| --- | --- | --- |
| AJIMEE-Bench | 182/200 (91.0%) | 183/200 (91.5%) |
| 日常文 | 79/81 | 79/81 |
| 慣用句 | 24/25 | 24/25 |
| ニュアンス | 16/20 | 16/20 |
| 打ち間違い | 14/40 | 14/40 |

計366問で、変更前に正解だった問題が不正解になった例はなかった。
1回の比較であり、1問の差から精度向上とは断定しない。実行時間はモデルの温まり方等が違うため速度比較に使わない。
記録: `C:\Users\aruik\kotori-first-check\release-eval`。

## CPUの初回候補

`KOTORI_LM_DEVICE=cpu python -X utf8 mozc/tools/first_candidate_smoke.py <session_handler_main.exe> --out <smoke-cpu.json>`。
ツールは出力されたcallbackのdelay_millisecに従って更新する。モデルを12秒温めた後の一例。
「あしをいためたので」の入力応答6.2ms。450ms後の更新1.7msでは候補なし、さらに450ms後の更新1.7msで
初めて「足を痛めたので」を表示。Space応答1.3msでも同じ文を変換した。
これはセッションツールの測定であり、TSFアプリでの描画遅延・コールドスタート全般を保証しない。
記録: `C:\Users\aruik\kotori-first-check\smoke-cpu.json`。

## 公開前に残る確認

- PR138のMSI CIと公開準備PRのCI。
- 使い捨てWindowsでMSI導入・TSF実入力・アンインストール（新しいinstaller_smoke.py）。
- 公開されたMSIのProductVersion・ハッシュ・同梱物。

未検証をPASSとは扱わない。予測の採用しきい値は暫定値で、校正した確率ではない。
