# 0051: カタカナ語から選ぶ英語候補の大規模辞書

- 日付: 2026-10-10
- 状態: 採用。ローカル候補検証済み、配布MSIは作成中。
- 関連: 0040、0050、カード53/64

## 問題

英語候補は手書き24表記に限られ、利用者から大規模辞書の採用を求められた。
綴りを推論モデルの同期生成に頼ると、キー応答時間・綴りの信頼性・PCごとの結果が不安定になる。

## 辞書と取得方法

[KEINOS/google-ime-user-dictionary-ja-en](https://github.com/KEINOS/google-ime-user-dictionary-ja-en)
のコミット7d241dafcf6ee1f9eafefc0ae7a929c095860246を採用。
EDICTを元に作られたコミュニティのカタカナ語英字辞典で、データはCC BY-SA 3.0。
Googleの製品辞書そのものではない。古いアーカイブのため、新語を網羅するとは言わない。

MODULE.bazelに6入力ファイルのURLとSHA-256を固定する。辞書原本や生成した大きな配列をGitへ入れない。
Bazelの生成処理で46,001行を読み、文字種の正規化、読み注釈の一致検査、英語説明の除去、
不正行・重複の除外、優先表記の補完を実施。同音異綴りは1読み4件まで保持する。
結果は31,068の読み、36,402組の読み・英語表記。
KotoriEnglish.tsvのSHA-256は91748ec2fa4bfe310793d38badbdb0c7b05aeff221e0241d91aaaa017fe1e6dd。

変更済みデータとC++配列もCC BY-SA 3.0で提供する。元辞書のコミュニティ、KEINOSと寄稿者、
Jim Breen/EDRDG、固定コミット、変更内容、ライセンスURLをNOTICEへ記載。
インストーラーにKotoriEnglish.tsv、KotoriEnglish-source.json、NOTICE-katakana-english.txtを同梱する。
データに対するライセンスをソフトウェア全体へ適用したとは記載しない。

## 候補処理

ソート済み静的配列を二分探索し、候補のカタカナ語に英字表記を追加する。
入力中のファイル読込み、通信、巨大な連想配列の初期化は不要。日本語の先頭候補は保持する。
付属語を保ち、重複を避け、追加候補へAI評価済み属性を継承しない。
既存ASCII候補の大小文字の順位を変えない。
先頭カタカナ語の正式英字が一覧の奥に既に存在する場合はその語の次へ移す。
accessibilityが深い位置にあるためa11yだけが初回表示される失敗を、この処理で解消した。

## 確認

EnglishVariantsRewriter全17テストPASS。27語をSuggestion/Prediction/Conversionで確認し、
light/rightの同音異綴り、付属語、重複、ASCII順位、正式英字の見える位置を検査。
実モデルと既存履歴のコピーでarchitecture、algorithm、orchestra、accessibility、collaboration、
configuration、schedule、programming、restaurant、chocolate、library、wirelessの12語が
初回候補/Tab/Space1の一覧に存在し、選択できることを確認した。
日本語の先頭を英字へ強制的に置換したという意味ではない。Windows実入力の検証ではない。

同じ最終ソースのStandard AJIMEE-Benchは183/200=91.5%で90%以上を維持。
117入力の正本/cache/新規cloneの同一性と全3パッチ適用を確認し、ローカルMSIへ進む。
詳細な原票はC:/Users/aruik/kotori-first-checkのlarge-english-*、english-visible-*、
history-english-cancel-final-v3.json。MSI版は6332として6331から更新できるようにする。
