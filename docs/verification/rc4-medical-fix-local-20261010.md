# 報告された「炒めて」「慰謝」の修正（2026-10-10）

BUILD6330/ソース25cd371のインストール済みファイルはMSIと同一だったが、利用者が
実入力で「脚を炒めてしまったため今日は医者に行こう」「脚を炒めてしまったので今日は慰謝に行こう」を報告した。
これは利用者観測の実入力FAILであり、以前のパッケージ/CLIの成功を実入力PASSとしない。
「ため/ので」が別入力かSpace回数かは確認待ち。接続詞の自動変更は未確定。

## 修正

1. 医者/慰謝のような無関係な同音語を、複数の漢字というだけで全文の優先候補へ昇格していた。
   説明できる語組だけを優先し、他の辞書候補は通常の文節内に保持する。特徴/特長等の機能と文節のまとまりは維持する。
2. 初回候補のタイマーにはアプリの周囲の文が含まれない。取り直しが空の文脈、Spaceが入力開始時の文脈を採点していた。
   取り直しのSuggest/PreviewもSpaceと同じclient_contextを使う。修正前に同じテストで前後の文の欠落を確認した。
3. WindowsのタイマーはGetBaseを現在の入力欄と比較していた。GetTopで現在の入力欄を取得し、
   非同期の編集セッション実行時にもフォーカスを再照合する。実アプリでの改善は新MSIの確認待ち。
   APIの根拠: https://learn.microsoft.com/en-us/windows/win32/tsf/edit-contexts
4. 既に6330が導入されているので、次のMSIはBUILD6331にする。REVISIONだけで更新済みとは扱わない。

## ローカル確認

- 単体: Session190、Nuance9、Engine86、全PASS。文脈の回帰は修正前FAIL→同じアサーションでPASS。
- 実モデル: 「ため」「ので」、それぞれ直前の文あり/なしの4ケースで初回候補=Space1、痛めて/医者。
  Space2は足/脚の通常の表記選択となり、痛めて/医者を保持。慰謝への優先移動はなくなった。
- AI準備後に待たずにSpace: 2ケースとも痛めて/医者、Space2でも保持。
- 料理の例: 初回/Space1で玉ねぎを炒めたので皿につけよう。Space2のひらがな「たまねぎ」でも炒めるを保持。
- 元の長文: Space1=特徴は、Space2=特長は。他の文字列は同一。変更箇所だけへフォーカス。
- Standard AJIMEE183/200=91.5%（31秒）。90%以上を維持。heldoutは再調整/反復評価に使っていない。
- BUILD6331を含む112入力は正本/cache/新規cloneで全バイト一致。0001〜0003を新規cloneへ適用確認。
  入力SHA-256: 9a458bb78212d52e16f03190ef760b3bc9115d02974c2658f324f59190b08d0d。
  定義: files順の相対path + TAB + file SHA-256 + LFをUTF-8にしてSHA-256。

## 未解決と公開境界

モデル読込み中に即Spaceを押すと通常変換へ戻り「炒めて」が残ることを6330で再現した。
今回、冷間時の全補正ができたとは主張しない。ユーザーの「炒めて」を全条件で説明したとの断定も避ける。
Windowsの初回候補/Tab/Spaceは同じ新MSIで実入力を確認する。現時点でこの修正版を実入力PASSや公開完了にしない。
GitHubのrc.4はdraftのまま。6330の不合格はdraft本文へも記録し、ソース/MSI/結果を固定して修正版を作る。

## 原票と失敗の保存

C:/Users/aruik/kotori-first-check/:

- user-medical-before-summary.json、user-medical-immediate-before-summary.json、user-medical-example-installed-files.json、user-medical-config-flags.json
- medical-context-regression-before.log（修正前FAIL）、medical-regressions-after.log、medical-binaries-after.log、medical-final-cli-build.log
- medical-model-after-final.json（5ケースの原票を同じEXEで照合して集約）、medical-cooking-after.json、medical-immediate-after.json
- medical-nuance-after-valid.json、medical-ajimee-after.jsonとmanifest/log/stderr
- medical-patches-after-shutdown.log、medical-source-manifest.json

測定スクリプトの最初の文脈fixtureは文字列の引用符不足で拒否され、読み不一致として失敗した。
そのdebug出力はmedical-harness-key-debug.json/.stderr.txtに保存。引用を修正しコマンド拒否を厳密に検出する。
料理の最初のSpace2条件は通常のひらがな表記を拒否していたため失敗。初回/Space1の条件は保ち、Space2でその表記を許す。
誤ったローマ字で送った長文のmedical-nuance-after.jsonは読みが異なるため採用しない。
読みを検査するmedical-nuance-after-valid.jsonを証拠とする。過去の失敗をPASSへ書き換えない。
