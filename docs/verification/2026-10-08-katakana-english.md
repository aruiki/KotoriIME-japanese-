# 英字候補の検証 (2026-10-08)

対象はPR140のEnglishVariantsRewriter修正。公開rc.2には未収録。
Mozc作業ツリーはC:\Users\aruik\mzfi、Google Mozcの基点はa069a88d。

## 実セッション

first_candidate_smoke.pyの--expect-variantで、最初に候補欄が現れた応答、Tab、Spaceの
各応答に指定したvalueが存在することをassertした。稼働中の利用者IMEには接続していない。

| 入力 | 必要な候補 | 初回 | Tab | Space |
| --- | --- | --- | --- | --- |
| indekkusu | index | PASS | PASS | PASS |
| efekuto | effect | PASS | PASS | PASS |
| inta-netto | internet | PASS | PASS | PASS |

修正前のindexは初回表示に存在せず、Space後だけに存在した。
修正後も日本語の先頭候補はインデックス・エフェクト・インターネットのまま。
初回入力要求の応答は3.1〜6.5ms、更新要求は1.3〜2.1ms。
環境の単発計測であり、性能向上の主張には使わない。
証跡はC:\Users\aruik\kotori-first-check\english-verified-*.json。

## 単体検証

EnglishVariantsRewriterのテストPASS。予測候補の属性、重複、付属語、content_valueの欠落、
全要求種別、文節境界とAI評価情報を誤ってコピーしないことを確認。
converter_mainとsession_handler_mainのリリースビルドPASS。
EnglishVariantsRewriter・LmRewriter・EngineConverter・Sessionの4テストターゲットPASS。
コマンドはbazelisk test //rewriter:english_variants_rewriter_test //rewriter:lm_rewriter_test
//engine:engine_converter_test //session:session_test --config release_build
--repo_env=BAZEL_LLVM=C:/Users/aruik/mz/src/third_party/llvm --test_output=errors。
ログはC:\Users\aruik\kotori-first-check\english-tests.log。更新後のMSI CIは確認中。

## 限界

追加表は24表記のみ。汎用の翻訳・綴り推定ではない。実アプリのTSF経由の確認は未完了。
