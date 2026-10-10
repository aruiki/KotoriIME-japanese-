# BUILD6334 ローカルMSI作成・内容照合（2026-10-10）

修正ソースコミット: e6e35a101fc2849a50489f41e757a471427b39b9。
Windows Installer版: 3.34.6334.100、前の公開6333からBUILD増加。
MSI: 1,569,173,504bytes、同梱48ファイル、未署名。
SHA-256: 7136ea32e39092ecdc7069cd0834e09d7fc0c2053fb89f3586410d5c8a7a599a。
入力マニフェスト: 3ca8f4653fe5e6fb058d3d9e2e99925e521cee78fd849bc3cf01a8330eca01d5。

全buildはローカル。//:packageは終了0、1035.5秒。
WiXで読取り専用展開し、必要ファイル/不要ファイル、梱包の版、compiled server/tool/TIP64、
モデル3件、実行環境18件、大規模英語辞書/NOTICE、元ソースのアイコン/背景/ショートカットを確認。
全payloadのSHAも同名JSONに保存。正本/cache/新規patch clone118入力と3パッチの一致を確認。
実モデル18例、最終4テスト対象、Standard183/200=91.5%との実行ファイル/モデル対応を照合した。

このMSIは公開前のローカル候補。正式版/新たなRCとしてGitHubへ公開していない。
導入先は利用者が入れたRC5の6333。今回の6334で自動上書きや再起動はしない。
RC5の設定保存表示は実画面で確認済みだが、6334 MSIの導入/更新/削除の確認ではない。
メモ帳は英数入力で、Kotoriの「あ」への切替えを利用者へ依頼中。日本語欄の初回候補/Tabは未確認。
正式版の完成判定はこの境界を残している。

成果物: C:/Users/aruik/kotori-first-check/corrected-alternatives-6334-release/Kotori64.msi。
同じフォルダーにsha256/source-manifest/validation/release-evidence/candidate-notesを保存。
低速なGitHubから1.57GBを再ダウンロードする必要はない。既存のRC5公開物は変更していない。
