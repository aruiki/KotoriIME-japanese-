# BUILD6334 補正後の別候補のローカル確認

RC5で「ちょとまってください」が先頭/Tab/Space1で直ってもSpace2で「ちょ止まってください」へ戻った。
検証した補正後の読みから、AIを呼ばないMozc変換で別候補を作り、補正前の候補より前へ入れる。
元の読みと候補を保持。補正候補はNO_LEARNING。ユーザー辞書の未採用補正にはこの情報を付けない。

最終ソース: 正本mzcorrection、build cache mzicons、新規upstream cloneの118入力は完全一致。
全3パッチの適用を確認。BUILDを6333から6334へ増加。モデル・辞書・品質設定の種類は不変。
入力マニフェスト: 3ca8f4653fe5e6fb058d3d9e2e99925e521cee78fd849bc3cf01a8330eca01d5。

engine_converter_test/candidate_test/lm_rewriter_test/english_variants_rewriter_testの4対象が通過。
検証は保護入力/AI無効/辞書失敗時フォールバック/補正メタデータの消去/ユーザー辞書の保持を含む。
初回のbuildはWSL bash誤選択で失敗し、Git bashを明示して修正。テスト1件は古いOutput再利用のため失敗。
実Sessionと同じコマンドごとのOutput初期化へ修正し、同じ候補切り替えの期待結果が通過。旧失敗原票も保持。

実モデルとこのPCの履歴コピーを専用プロファイルで使用。履歴rewriterは有効。18例が通過。
入力確定はしない。原本の履歴/辞書や利用者設定は変更しない。
- 足を痛めた/医療のため・ので: 初回候補/Tab/Space1一致、Space2も痛めた・医者を維持。
- 玉ねぎを炒めた: 炒めるを維持。
- ちょとまってください: 初回/Tab/Space1はちょっと待ってください、Space2はちょっとまってください。
- 長文: Space2で特徴から特長へ、他の部分を維持。
- 大規模辞書の英語12語: 候補とSpace2で英語を維持。

Standard、同梱LLM/zenz、ビーム4のAJIMEE-Bench200問は183/200=91.5%（contextあり、35秒）。
90%以上の条件を維持。前の結果を新しいコードの結果として流用していない。
Session EXE SHA: 14c4ed0eb4d407b00262c371df6151cd6a5f685014c6d39c09c902f4ebf7f84b。
Converter SHA: 543b041396ed83ca1ae98801a44c35af436f2b10b463b0b1046751caa014fc3a。
同名JSONへ結果を記録。生の履歴コピー・入力イベントはGitへ入れない。

これらはローカルSession/Converterの確認。Windows TSFの実際の初回表示とTabの確認ではない。
導入6333の設定UIはrc5-native-settings-and-computer-use-20261010で別途確認。
新しい6334 MSIの導入/更新/削除、冷間直後の候補、別PC/CPUの受入れは未確認。
