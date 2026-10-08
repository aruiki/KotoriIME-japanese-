# 2026-10-08 初回候補と候補欄の開発確認

配布版の受け入れ確認ではない。未インストールの開発ビルドを、独立した一時プロファイルで実行した。

## 対象

- wrapper基準: `270d67c28e6a84522c8719e047e74b6c919baea9`
- Mozc基準: `a069a88d4cb5c011de0f9aebb6c149a1c808d904`
- 作業: `codex/first-candidate`、Mozc別作業ツリー `C:\Users\aruik\mzfi`
- session_handler_main.exe SHA-256: `3A4917FE14FA8CB8AEC84B759EEEB1922FCB3E384FF42DF26D275C51A2716F90`
- モデル・ランタイム: インストール済みKotoriのローカルファイル。GPU使用、既定設定。

## 実行結果

`first_candidate_smoke.py` は実セッションへ入力し、初回出力と遅延更新を別々に記録する。
従来のsession_handler_mainはタイマー要求を即実行していたため、初回出力と更新後出力を区別できなかった。
このテスト用ツールの動作も修正した。したがって、旧ツールとの単純な時間差を性能改善値としては扱わない。

モデル準備後に `ashiwoitametanode` を送った結果:

| 出力 | 最初の候補 | 要求応答時間 |
| --- | --- | ---: |
| 打鍵直後 | 未表示、読みは「あしをいためたので」 | 11.1 ms（文字列の一括入力） |
| 200 ms待った後の更新 | 未表示 | 3.0 ms |
| さらに800 ms後の更新 | 足を痛めたので | 2.0 ms |
| 続く3回の更新 | 足を痛めたので | 2.5〜3.0 ms |
| Space | 未確定文「足を」「痛めたので」 | 1.2 ms |

測定は1回・1文。約1秒の候補表示待ちと、各要求の応答時間は別の値。
TSF、Word、ブラウザなどでの実際の描画遅延は未測定。
変更途中の同期プレビューでは数秒待つ例があり、そのまま採用せず、文候補のコピーを使う非同期評価へ変更した。

## ビルド・テスト

Windowsで `bazelisk`、`--config release_build`、
`--repo_env=BAZEL_LLVM=C:/Users/aruik/mz/src/third_party/llvm` を使用。

- ビルドPASS: converter_main、session_handler_main、Windows renderer、kotori_candidate_snapshot。
- テストPASS: session_test、engine_converter_test、lm_rewriter_test、candidate_test、
  kotori_diagnostics_test、win32_renderer_util_test（6ターゲット）。
- 新規確認: 初回候補を待つ間の読みの表示、強い予測の優先、AI無効・シークレット、評価失敗時の上限と復帰。
- 既存の副候補欄専用テストは、カスケード有効を明示して従来の選択動作を検証するよう変更。
- 100%・200%の実描画を画像にして目視確認。文字の欠け・重なりなし。

## 未完了

- 予測の暫定採用条件のデータ評価。現在の数値を「高い正解確率」と説明しない。
- AJIMEE・日常・打ち間違い・負荷の前後比較、CPU条件。
- 編集中の世代交代・フォーカス移動を含む実アプリのTSF確認。
- インストーラー、CI、配布更新。
- LLMによる自由な文章補正生成、カタカナから英語への変換。

ログと生の出力は開発機の `C:\Users\aruik\kotori-first-check` に保存。
既存のIMEの停止・差し替え・インストールは行っていない。
